from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import select, Session
from passlib.hash import bcrypt

from app.models.user_model import User
from app.db.postgresql import get_db
from app.auth.jwt_handler import create_access_token
from app.auth.otp_service import send_otp, verify_otp

router = APIRouter()

@router.post("/send-otp")
def send_otp_endpoint(mobile: str):
    otp = send_otp(mobile)
    return {"message": f"OTP sent to {mobile}", "demo_otp": otp}

@router.post("/verify-otp")
def verify_otp_endpoint(mobile: str, otp: str, db: Session = Depends(get_db)):
    if not verify_otp(mobile, otp):
        raise HTTPException(status_code=401, detail="Invalid OTP")

    user = db.exec(select(User).where(User.mobile == mobile)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_access_token({"user_id": user.user_id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
def login(identifier: str, password: str, db: Session = Depends(get_db)):
    query = select(User).where(
        (User.email == identifier) |
        (User.user_id == identifier) |
        (User.mobile == identifier) |
        (User.aadhar_number == identifier)
    )
    user = db.exec(query).first()

    if not user or not bcrypt.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.user_id})
    return {"access_token": token, "token_type": "bearer"}
