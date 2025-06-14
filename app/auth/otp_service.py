import random
import requests
from typing import Dict
import os
# load_dotenv() 
otp_store: Dict[str, str] = {}

# FAST2SMS_API_KEY = "rnPdHGXOYE592ZxUzhTuDkJCv7fiwA6y4FRQcWe3alBKVpL8oI9AdM7lhnjb5uKIagZmsiQr0TwBetLk"

def send_otp(mobile: str) -> str:
    otp = str(random.randint(100000, 999999))
    otp_store[mobile] = otp

    payload = {
        'authorization': os.getenv("FAST2SMS_API_KEY"),
        'sender_id': 'FSTSMS',
        'message': f"Your OTP is {otp}",
        'language': 'english',
        'route': 'qt',  # 'qt' for quick transactional route
        'numbers': mobile,
    }

    headers = {
        'cache-control': "no-cache"
    }

    response = requests.post("https://www.fast2sms.com/dev/bulkV2", data=payload, headers=headers)
    print("OTP Send Status:", response.json())
    return otp

def verify_otp(mobile: str, otp: str) -> bool:
    return otp_store.get(mobile) == otp
