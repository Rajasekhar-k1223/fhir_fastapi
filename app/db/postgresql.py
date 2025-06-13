from sqlmodel import create_engine, Session
from app.models.user_model import User

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost/dbname"
engine = create_engine(DATABASE_URL)

async def get_db():
    with Session(engine) as session:
        yield session
