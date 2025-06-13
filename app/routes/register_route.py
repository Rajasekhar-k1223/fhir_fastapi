from fastapi import APIRouter, Depends,HTTPException
from sqlmodel import Session
from passlib.hash import bcrypt
from app.db.postgresql import get_db
from app.models.user_model import User
from app.models.patient_model import Patient
from app.models.pracitioner_model import Practitioner
from app.schemas.UserRegisterSchema import UserRegisterSchema
import random


router = APIRouter()

def generate_user_id() -> str:
    import random
    return str(random.randint(100000, 999999))

@router.post("/register")
def register_user(data: UserRegisterSchema, db: Session = Depends(get_db)):
    # ✅ Check for existing email
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Optional: Check for duplicate mobile
    if db.query(User).filter(User.mobile == data.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    # ✅ Optional: Check for duplicate Aadhar
    if data.aadhar and db.query(User).filter(User.aadhar_number == data.aadhar).first():
        raise HTTPException(status_code=400, detail="Aadhar number already registered")

    # Generate user_id
    user_id = generate_user_id()

    # Create user
    user = User(
        user_id=user_id,
        email=data.email,
        mobile=data.mobile,
        aadhar_number=data.aadhar,
        username=data.username,
        password=bcrypt.hash(data.password),
        role=data.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Create related practitioner or patient
    if data.role.lower() == "doctor":
        doctor = Practitioner(user_id=user.user_id, name=user.username, mobile=user.mobile)
        db.add(doctor)
    else:
        patient = Patient(user_id=user.user_id, name=user.username, mobile=user.mobile)
        db.add(patient)

    db.commit()

    return {
        "message": "User registered successfully",
        "user_id": user.user_id
    }
