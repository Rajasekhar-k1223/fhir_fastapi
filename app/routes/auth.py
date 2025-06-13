from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.services.auth import create_access_token, verify_password
from app.db.postgresql import get_db
from app.models.user_model import User

router = APIRouter()

@router.post("/login")
async def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.exec(select(User).where(User.email == email)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
