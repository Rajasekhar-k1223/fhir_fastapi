from fastapi import APIRouter, Depends
from sqlmodel import Session
from passlib.hash import bcrypt
from app.models.user_model import User
from app.db.postgresql import get_db

router = APIRouter()

def generate_user_id() -> str:
    import random
    return str(random.randint(100000, 999999))

@router.post("/register")
def register_user(data: dict, db: Session = Depends(get_db)):
    user_id = generate_user_id()

    user = User(
        user_id=user_id,
        email=data.get("email"),
        mobile=data.get("mobile"),
        aadhar_number=data.get("aadhar"),
        username=data.get("username"),
        password=bcrypt.hash(data["password"]),
        role=data.get("role", "patient")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User registered", "user_id": user.user_id}
