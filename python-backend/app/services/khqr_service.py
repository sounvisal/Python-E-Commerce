import os
import json
import subprocess
import asyncio
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from app.models.order import Order

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

def build_instant_bakong_khqr(amount: float, order_number: str = "LUM-000000", merchant_name: str = "SUON VISAL") -> str:
    """
    Generates a 100% compliant Dynamic Bakong KHQR (EMVCo TLV format)
    configured for ABA Bank (merchant account 0016abaakhppxxx@abaa).
    """
    amt_str = f"{amount:.2f}"
    
    # Tag 30: Merchant Account Information (ABA Bank Bakong)
    # Subtag 00: Global Unique Identifier "abaakhppxxx@abaa" (len: 16)
    # Subtag 01: Account/Merchant ID "126052613334027" (len: 15)
    # Subtag 02: Acquiring Bank "ABA Bank" (len: 8)
    sub_00 = "0016abaakhppxxx@abaa"
    sub_01 = "0115126052613334027"
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
    First attempts live generation via ABA PayWay bridge with a short timeout.
    If unavailable or timed out, falls back instantly to the EMVCo generator.
    """
    # Default instant fallback
    instant_qr = build_instant_bakong_khqr(amount, order_number)
    
    if not try_live:
        return {
            "success": True,
            "qr_string": instant_qr,
            "amount": amount,
            "currency": "USD",
            "merchant_name": "SUON VISAL",
            "order_number": order_number,
            "client_id": None,
            "source": "instant_emvco",
            "payway_url": "https://link.payway.com.kh/ABAPAYaC455755m"
        }

    # Attempt live bridge
    bridge_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "..", "payway_bridge.js")
    bridge_path = os.path.abspath(bridge_path)

    if os.path.exists(bridge_path):
        try:
            # Run node bridge with 12s timeout
            proc = await asyncio.create_subprocess_exec(
                "node", bridge_path, "generate", str(amount), "https://link.payway.com.kh/ABAPAYaC455755m",
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
                        "merchant_name": "SUON VISAL",
                        "order_number": order_number,
                        "client_id": res.get("client_id"),
                        "source": "live_aba_payway",
                        "payway_url": "https://link.payway.com.kh/ABAPAYaC455755m"
                    }
        except Exception:
            pass  # Fall back to instant_qr

    return {
        "success": True,
        "qr_string": instant_qr,
        "amount": amount,
        "currency": "USD",
        "merchant_name": "SUON VISAL",
        "order_number": order_number,
        "client_id": None,
        "source": "instant_emvco",
        "payway_url": "https://link.payway.com.kh/ABAPAYaC455755m"
    }
