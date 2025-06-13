from sqlmodel import SQLModel, Field
from typing import Optional
import uuid


class PGPractitioner(SQLModel, table=True):
    __tablename__ = "practitioner"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    name: str
    mobile: str
    created_at: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))

    class Config:
        from_attributes = True
