# app/models/pg_patient_model.py

from sqlmodel import SQLModel, Field

class PGPatient(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str
    name: str
    mobile: str
