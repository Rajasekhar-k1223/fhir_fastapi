from sqlmodel import SQLModel, Field
from typing import Optional
import uuid

class PGPatient(SQLModel, table=True):
    __tablename__ = "patients"
    __table_args__ = {"extend_existing": True}
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    username: str
    mobile: str
    aadhar_number:str
    created_at: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True