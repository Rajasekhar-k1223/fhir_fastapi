from sqlmodel import SQLModel, Field
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)             # 6+ digit custom ID
    email: Optional[str] = Field(default=None, index=True, unique=True)
    mobile: Optional[str] = Field(default=None, index=True, unique=True)
    aadhar_number: Optional[str] = Field(default=None, index=True, unique=True)
    username: Optional[str] = Field(default=None)
    password: str                                              # Hashed
    role: str = "patient"
    is_active: bool = True