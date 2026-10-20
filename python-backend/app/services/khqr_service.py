import os
import json
import asyncio
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.order import Order

DEFAULT_MERCHANT_NAME = os.getenv("BAKONG_MERCHANT_NAME", "LUMEA ATELIER")
DEFAULT_MERCHANT_ID = os.getenv("BAKONG_ACCOUNT_ID", "000000000000000")
DEFAULT_PAYWAY_URL = os.getenv("ABA_PAYWAY_URL", "")

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

async def get_bakong_khqr_data(amount: float, order_number: str = "LUM-000000", try_live: bool = True) -> Dict[str, Any]:
    """
    Obtains KHQR payment data.
    If ABA_PAYWAY_URL is configured in environment, attempts bridge generation.
    Otherwise, instantly returns compliant Dynamic Bakong KHQR.
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

    # Attempt live bridge only if payway_url is configured and script exists
    bridge_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "..", "payway_bridge.js")
    bridge_path = os.path.abspath(bridge_path)

    if os.path.exists(bridge_path):
        try:
            proc = await asyncio.create_subprocess_exec(
                "node", bridge_path, "generate", str(amount), payway_url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=14.0)
            if stdout:
                res = json.loads(stdout.decode("utf-8").strip())
                if res.get("success") and res.get("qr_string"):
                    return {
                        "success": True,
                        "qr_string": res["qr_string"],
                        "amount": amount,
                        "currency": "USD",
                        "merchant_name": merchant_name,
                        "order_number": order_number,
                        "client_id": res.get("client_id"),
                        "source": "live_aba_payway",
                        "payway_url": payway_url
                    }
        except Exception:
            pass

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
