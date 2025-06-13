from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    username: str
    email: Optional[str]
    mobile: str
    aadhar_number: Optional[str]
    password: str
    role: str
    is_active: bool = True

class Patient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    name: str
    mobile: str

class Practitioner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str
    name: str
    mobile: str