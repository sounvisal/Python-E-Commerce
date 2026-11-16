import os
import sys
import json
import asyncio
import subprocess
import logging
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from app.core.database import SessionLocal
from app.models.order import Order
from app.services.order_lifecycle import settle_payment

logger = logging.getLogger("lumea.khqr")

# Load local environment if present (gitignored)
load_dotenv()

DEFAULT_MERCHANT_NAME = os.getenv("BAKONG_MERCHANT_NAME", "LUMEA ATELIER")
DEFAULT_MERCHANT_ID = os.getenv("BAKONG_ACCOUNT_ID", "000000000000000")
DEFAULT_PAYWAY_URL = os.getenv("ABA_PAYWAY_URL", "")

# Registry for active live background monitoring processes: order_number -> subprocess.Popen
ACTIVE_PAYMENT_PROCS: Dict[str, subprocess.Popen] = {}

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
    
    # Tag 30: Merchant Account Information
    sub_00 = "0016abaakhppxxx@abaa"
    sub_01 = f"01{len(account_id):02d}{account_id}"
    sub_02 = "0208ABA Bank"
    tag_30_val = f"{sub_00}{sub_01}{sub_02}"
    tag_30 = f"30{len(tag_30_val):02d}{tag_30_val}"

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
    tag_60 = "6003N/A"

    # Tag 62: Additional Data Field Template (Bill/Order Reference)
    bill_sub = f"01{len(order_number):02d}{order_number}"
    payway_sub = "0010PAYWAY@ABA"
    tag_62_val = f"{payway_sub}{bill_sub}"
    tag_62 = f"62{len(tag_62_val):02d}{tag_62_val}"

    # Construct payload without CRC
    raw_payload = f"000201010212{tag_30}{tag_52}{tag_53}{tag_54}{tag_58}{tag_59}{tag_60}{tag_62}6304"
    crc = crc16_emvco(raw_payload)
    return f"{raw_payload}{crc}"

def _sync_watch_approval(proc: subprocess.Popen, order_number: str):
    """
    Synchronous worker executed in background thread to monitor PayWay approval.
    """
    logger.info(f"Started live PayWay background monitoring thread for order {order_number}...")
    try:
        while proc.poll() is None:
            line = proc.stdout.readline()
            if not line:
                break
            text = line.strip()
            if not text:
                continue
            try:
                data = json.loads(text)
                event = data.get("event")
                if event == "paid" or data.get("action") == "approved":
                    client_id = data.get("client_id") or "LIVE"
                    logger.info(f"Payment APPROVED for {order_number}! Client ID: {client_id}")

                    # Mark order as Paid in database
                    db = SessionLocal()
                    try:
                        order = db.query(Order).filter(Order.order_number == order_number).first()
                        if order:
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
        ACTIVE_PAYMENT_PROCS.pop(order_number, None)
        try:
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass

def cancel_payment_session(order_number: str):
    """Cancels and terminates any running background browser session for this order."""
    proc = ACTIVE_PAYMENT_PROCS.pop(order_number, None)
    if proc:
        try:
            if proc.poll() is None:
                proc.kill()
        except Exception:
            pass

async def get_bakong_khqr_data(amount: float, order_number: str = "LUM-000000", try_live: bool = True) -> Dict[str, Any]:
    """
    Obtains KHQR payment data.
    If ABA_PAYWAY_URL is configured in environment, extracts authentic live ABA PayWay QR
    via the Playwright bridge in a non-blocking worker thread.
    Otherwise, returns compliant Dynamic Bakong KHQR.
    """
    merchant_name = os.getenv("BAKONG_MERCHANT_NAME", DEFAULT_MERCHANT_NAME)
    payway_url = os.getenv("ABA_PAYWAY_URL", DEFAULT_PAYWAY_URL)
    instant_qr = build_instant_bakong_khqr(amount, order_number, merchant_name)
    
    if not try_live or not payway_url:
        return {
            "success": True,
            "qr_string": instant_qr,
            "amount": amount,
            "currency": "USD",
            "merchant_name": merchant_name,
            "order_number": order_number,
            "client_id": None,
            "source": "instant_emvco",
            "payway_url": payway_url or ""
        }

    # Locate bridge script (prefers extract_full_data.js, falls back to payway_bridge.js)
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    bridge_script = os.path.join(root_dir, "extract_full_data.js")
    if not os.path.exists(bridge_script):
        bridge_script = os.path.join(root_dir, "payway_bridge.js")

    if os.path.exists(bridge_script):
        cancel_payment_session(order_number)

        try:
            logger.info(f"Extracting live ABA PayWay KHQR for {order_number} (${amount:.2f}) via {bridge_script}...")

            # Use subprocess.Popen with thread execution to guarantee 100% Windows asyncio compatibility
            proc = subprocess.Popen(
                ["node", bridge_script, "session", str(amount), order_number, payway_url],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1
            )

            # Read line 1 asynchronously in a worker thread
            def _read_first_line():
                return proc.stdout.readline()

            line = await asyncio.wait_for(asyncio.to_thread(_read_first_line), timeout=25.0)

            if line:
                res = json.loads(line.strip())
                if (res.get("event") == "qr_ready" or res.get("success")) and res.get("qr_string"):
                    ACTIVE_PAYMENT_PROCS[order_number] = proc

                    # Spawn background monitoring thread to detect customer payment approval
                    asyncio.create_task(asyncio.to_thread(_sync_watch_approval, proc, order_number))

                    return {
                        "success": True,
                        "qr_string": res["qr_string"],
                        "amount": amount,
                        "currency": "USD",
                        "merchant_name": res.get("merchant_name") or merchant_name,
                        "order_number": order_number,
                        "client_id": res.get("client_id"),
                        "source": "live_aba_payway",
                        "payway_url": payway_url
                    }
                else:
                    logger.warning(f"Bridge returned non-ready response: {res}")
            else:
                logger.warning("Bridge returned empty stdout.")
        except Exception as ex:
            logger.exception(f"Live PayWay extraction exception: {ex}")

    return {
        "success": True,
        "qr_string": instant_qr,
        "amount": amount,
        "currency": "USD",
        "merchant_name": merchant_name,
        "order_number": order_number,
        "client_id": None,
        "source": "instant_emvco",
        "payway_url": payway_url or ""
    }
