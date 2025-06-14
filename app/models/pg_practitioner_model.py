from sqlmodel import SQLModel, Field
from typing import Optional
import uuid
from datetime import datetime

class PGPractitioner(SQLModel, table=True):
    __tablename__ = "practitioners"
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    username: str
    mobile: str
    aadhar_number:str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True
