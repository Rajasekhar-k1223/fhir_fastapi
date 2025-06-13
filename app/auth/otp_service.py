import random
import requests
from typing import Dict

otp_store: Dict[str, str] = {}

def send_otp(mobile: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_store[mobile] = otp

    response = requests.post("https://textbelt.com/text", {
        "phone": mobile,
        "message": f"Your OTP is: {otp}",
        "key": "textbelt"
    })

    print("OTP Send Status:", response.json())  # Log status
    return otp

def verify_otp(mobile: str, otp: str) -> bool:
    return otp_store.get(mobile) == otp
