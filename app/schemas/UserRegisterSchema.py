from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegisterSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    mobile: str
    aadhar: Optional[str] = None
    password: str
    role: Optional[str] = "patient"
