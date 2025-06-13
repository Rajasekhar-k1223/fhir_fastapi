from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from passlib.hash import bcrypt
from pymongo import MongoClient
from app.db.postgresql import get_db
from app.models.user_model import User
from app.models.patient_model import Patient as PGPatient
from app.models.pracitioner_model import Practitioner as PGPractitioner
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
        # PostgreSQL entry
        doctor = PGPractitioner(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            mobile=user.mobile,
            aadhar_number=user.aadhar_number
        )
        db.add(doctor)
        db.commit()

        # MongoDB (FHIR-style)
        fhir_doctor_doc = {
            "resourceType": "Practitioner",
            "id": str(ObjectId()),
            "identifier": [{"value": user.user_id}],
            "name": [{"text": user.username}],
            "telecom": [{"system": "phone", "value": user.mobile}],
            "meta": {"source": "registration-api"}
        }
        practitioner_collection.insert_one(fhir_doctor_doc)

    else:
        # PostgreSQL entry
        patient = PGPatient(
            user_id=user.user_id,
            username=user.username,
            email=user.email,
            mobile=user.mobile,
            aadhar_number=user.aadhar_number
        )
        db.add(patient)
        db.commit()

        # MongoDB (FHIR-style)
        fhir_patient_doc = {
            "resourceType": "Patient",
            "id": str(ObjectId()),
            "identifier": [{"value": user.user_id}],
            "name": [{"text": user.username}],
            "telecom": [{"system": "phone", "value": user.mobile}],
            "meta": {"source": "registration-api"}
        }
        patient_collection.insert_one(fhir_patient_doc)

    return {
        "message": "User registered successfully",
        "user_id": user.user_id
    }
