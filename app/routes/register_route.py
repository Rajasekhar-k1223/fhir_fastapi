from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from passlib.hash import bcrypt
from pymongo import MongoClient
from app.db.postgresql import get_db
from app.models.user_model import User
from app.models.patient_model import PatientResource
from app.models.pracitioner_model import PractitionerResource
from app.schemas.UserRegisterSchema import UserRegisterSchema
from app.db.mongo import patient_collection, practitioner_collection
import random
from bson import ObjectId

router = APIRouter()

# ✅ Generate 6-digit user_id
def generate_user_id() -> str:
    return str(random.randint(100000, 999999))

@router.post("/register")
def register_user(data: UserRegisterSchema, db: Session = Depends(get_db)):
    # ✅ Check for existing email
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # ✅ Check for duplicate mobile
    if db.query(User).filter(User.mobile == data.mobile).first():
        raise HTTPException(status_code=400, detail="Mobile number already registered")

    # ✅ Check for duplicate Aadhar
    if data.aadhar and db.query(User).filter(User.aadhar_number == data.aadhar).first():
        raise HTTPException(status_code=400, detail="Aadhar number already registered")

    # ✅ Generate user_id
    user_id = generate_user_id()

    # ✅ Create User in PostgreSQL
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

    # ✅ Save Patient or Practitioner to PostgreSQL and MongoDB
    if data.role.lower() == "doctor":
        fhir_data = {}  # Optional: extend with FHIR-compliant fields
        practitioner_resource = PractitionerResource(fhir_data, user.user_id, user.username, user.mobile,user.aadhar_number)
        practitioner_resource.save_to_postgres(db)
        practitioner_resource.save_to_mongodb()
    else:
        fhir_data = {}
        patient_resource = PatientResource(fhir_data, user.user_id, user.username, user.mobile,user.aadhar_number)
        patient_resource.save_to_postgres(db)
        patient_resource.save_to_mongodb()
    return {
        "message": "User registered successfully",
        "user_id": user.user_id
    }
