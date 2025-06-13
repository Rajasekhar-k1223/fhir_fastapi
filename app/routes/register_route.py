from fastapi import APIRouter, Depends
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
    user_id = generate_user_id()

    # Create User record
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

    # Create related Patient or Doctor record
    if data.role.lower() == "doctor":
        doctor = Practitioner(user_id=user.user_id, name=user.username, mobile=user.mobile)
        db.add(doctor)
    else:
        patient = Patient(user_id=user.user_id, name=user.username, mobile=user.mobile)
        db.add(patient)

    db.commit()
    return {"message": "User registered", "user_id": user.user_id}
