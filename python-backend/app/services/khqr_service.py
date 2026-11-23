import os
import json
import asyncio
import subprocess
import logging
from typing import Optional, Dict, Any
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv
from app.core.database import SessionLocal
from app.models.order import Order
from app.services.order_lifecycle import settle_payment
from app.core.config import settings

logger = logging.getLogger("lumea.khqr")

# Load local environment if present (gitignored)
load_dotenv()

DEFAULT_MERCHANT_NAME = os.getenv("BAKONG_MERCHANT_NAME", "LUMEA ATELIER")
DEFAULT_MERCHANT_ID = os.getenv("BAKONG_ACCOUNT_ID", "000000000000000")

# Registry for active live background monitoring processes: order_number -> subprocess.Popen
ACTIVE_PAYMENT_PROCS: Dict[str, subprocess.Popen] = {}
LOCAL_PAYMENT_QRS: Dict[str, Dict[str, Any]] = {}

def crc16_emvco(data: str) -> str:
    """
    Computes standard CRC16-CCITT (polynomial 0x1021, init 0xFFFF)
    per EMVCo and National Bank of Cambodia (NBC) Bakong KHQR specifications.
    """
    crc = 0xFFFF
    for byte in data.encode("utf-8"):
        crc ^= (byte << 8)
        for _ in range(8):
            if crc & 0x8000:
                crc = ((crc << 1) ^ 0x1021) & 0xFFFF
            else:
                crc = (crc << 1) & 0xFFFF
    return f"{crc:04X}"

def matches_order_qr(qr, amount):
    if not isinstance(qr, str) or not qr.startswith("000201") or len(qr) > 4096:
        return False
    if not qr.endswith(crc16_emvco(qr[:-4])):
        return False
    fields = {}
    offset = 0
    while offset + 4 <= len(qr):
        tag, size = qr[offset:offset + 2], qr[offset + 2:offset + 4]
        if not tag.isascii() or not tag.isdigit() or not size.isascii() or not size.isdigit() or tag in fields:
            return False
        end = offset + 4 + int(size)
        if end > len(qr):
            return False
        fields[tag] = qr[offset + 4:end]
        offset = end
    try:
        return (
            offset == len(qr) and tag == "63" and size == "04" and fields.get("53") == "840"
            and Decimal(fields.get("54", "")) == Decimal(str(amount))
        )
    except InvalidOperation:
        return False

def build_instant_bakong_khqr(
    amount: float,
    order_number: str = "LUM-000000",
    merchant_name: Optional[str] = None
) -> str:
    """
    Generates a 100% compliant Dynamic Bakong KHQR (EMVCo TLV format)
    configured for Luméa Atelier digital checkout.
    """
    if not merchant_name:
        merchant_name = os.getenv("BAKONG_MERCHANT_NAME", DEFAULT_MERCHANT_NAME)
    
    account_id = os.getenv("BAKONG_ACCOUNT_ID", DEFAULT_MERCHANT_ID)
    
    amt_str = f"{amount:.2f}"
    
    # Tag 29 (Individual Bakong Account) vs Tag 30 (Merchant Account)
    if "@" in account_id:
        sub_00 = f"00{len(account_id):02d}{account_id}"
        acc_tag = f"29{len(sub_00):02d}{sub_00}"
    else:
        # Tag 30: Merchant Account Information
        sub_00 = "0016abaakhppxxx@abaa"
        sub_01 = f"01{len(account_id):02d}{account_id}"
        sub_02 = "0208ABA Bank"
        tag_30_val = f"{sub_00}{sub_01}{sub_02}"
        acc_tag = f"30{len(tag_30_val):02d}{tag_30_val}"

    # Tag 52: Merchant Category Code (5912: Drug Stores & Pharmacies / Beauty or 7832)
    tag_52 = "52047832"

    # Tag 53: Transaction Currency (840 = USD)
    tag_53 = "5303840"

    # Tag 54: Transaction Amount
    tag_54 = f"54{len(amt_str):02d}{amt_str}"

    # Tag 58: Country Code (KH)
    tag_58 = "5802KH"

    # Tag 59: Merchant Name
    m_name = merchant_name[:25].upper()
    tag_59 = f"59{len(m_name):02d}{m_name}"

    # Tag 60: Merchant City
    tag_60 = "6010PHNOM PENH"

    # Tag 62: Additional Data Field Template (Bill/Order Reference)
    bill_sub = f"01{len(order_number):02d}{order_number}"
    payway_sub = "0010PAYWAY@ABA"
    tag_62_val = f"{payway_sub}{bill_sub}"
    tag_62 = f"62{len(tag_62_val):02d}{tag_62_val}"

    # Construct payload without CRC
    raw_payload = f"000201010212{acc_tag}{tag_52}{tag_53}{tag_54}{tag_58}{tag_59}{tag_60}{tag_62}6304"
    crc = crc16_emvco(raw_payload)
    return f"{raw_payload}{crc}"

def _sync_watch_approval(proc: subprocess.Popen, order_number: str, client_id: str):
    """
    Synchronous worker executed in background thread to monitor PayWay approval.
    """
    logger.info(f"Started live PayWay background monitoring thread for order {order_number}...")
    try:
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            text = line.strip()
            if not text:
                continue
            try:
                data = json.loads(text)
                event = data.get("event")
                if event == "paid" and data.get("order_number") == order_number and data.get("client_id") == client_id:
                    db = SessionLocal()
                    try:
                        order = db.query(Order).filter(Order.order_number == order_number).first()
                        if order and order.payment_method == 'khqr' and not order.payway_gateway:
                            settle_payment(db, order, f"ABA-LIVE-{client_id}")
                            db.commit()
                    finally:
                        db.close()
                    break
                elif event == "timeout":
                    logger.info(f"PayWay session timed out (5 mins) for order {order_number}")
                    break
            except json.JSONDecodeError:
                pass
    except Exception as e:
        logger.warning(f"PayWay monitor thread exception for {order_number}: {e}")
    finally:
        if ACTIVE_PAYMENT_PROCS.get(order_number) is proc:
            ACTIVE_PAYMENT_PROCS.pop(order_number, None)
            LOCAL_PAYMENT_QRS.pop(order_number, None)
        try:
            if proc.poll() is None:
                proc.kill()
            proc.wait()
        except Exception:
            pass

def cancel_payment_session(order_number: str):
    """Cancels and terminates any running background browser session for this order."""
    proc = ACTIVE_PAYMENT_PROCS.pop(order_number, None)
    LOCAL_PAYMENT_QRS.pop(order_number, None)
    if proc:
        try:
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass

async def get_bakong_khqr_data(amount: float, order_number: str = "LUM-000000", try_live: bool = True) -> Dict[str, Any]:
    """Local PayWay link integration. Hosted checkout uses the merchant API."""
    payway_url = os.getenv("ABA_PAYWAY_URL", "")
    if not try_live or not payway_url:
        return {"success": False, "source": "unavailable"}
    if order_number in LOCAL_PAYMENT_QRS:
        return LOCAL_PAYMENT_QRS[order_number]
    for num, p in list(ACTIVE_PAYMENT_PROCS.items()):
        if p.poll() is not None:
            ACTIVE_PAYMENT_PROCS.pop(num, None)
    if order_number in ACTIVE_PAYMENT_PROCS or len(ACTIVE_PAYMENT_PROCS) >= 3:
        return {"success": False, "source": "unavailable"}

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    bridge_script = os.path.join(root_dir, "scripts", "khqr", "payway-bridge.cjs")
    proc = None
    watching = False
    try:
        proc = subprocess.Popen(
            ["node", bridge_script, f"{amount:.2f}", order_number],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        ACTIVE_PAYMENT_PROCS[order_number] = proc
        line = await asyncio.wait_for(asyncio.to_thread(proc.stdout.readline), timeout=35)
        data = json.loads(line)
        client_id = data.get("client_id")
        if (
            data.get("event") != "qr_ready" or data.get("order_number") != order_number
            or not isinstance(client_id, str) or not client_id or not matches_order_qr(data.get("qr_string"), amount)
        ):
            return {"success": False, "source": "unavailable"}
        qr_data = {
            "success": True,
            "qr_string": data["qr_string"],
            "amount": amount,
            "currency": "USD",
            "merchant_name": data.get("merchant_name") or DEFAULT_MERCHANT_NAME,
            "order_number": order_number,
            "client_id": client_id,
            "source": "live_aba_payway",
        }
        LOCAL_PAYMENT_QRS[order_number] = qr_data
        asyncio.create_task(asyncio.to_thread(_sync_watch_approval, proc, order_number, client_id))
        watching = True
        return qr_data
    except (OSError, ValueError, TimeoutError):
        logger.warning("Could not open a local PayWay payment session for %s.", order_number)
        return {"success": False, "source": "unavailable"}
    finally:
        if proc is not None and not watching:
            if ACTIVE_PAYMENT_PROCS.get(order_number) is proc:
                ACTIVE_PAYMENT_PROCS.pop(order_number, None)
            if proc.poll() is None:
                proc.kill()
            proc.wait()
