from sqlmodel import create_engine, Session
from app.models.user_model import User

DATABASE_URL = "postgresql://postgres:pnQgJJPXsAUwhNMKpfthUwhmxOTovupn@caboose.proxy.rlwy.net:35090/railway"

engine = create_engine(DATABASE_URL, echo=True)  # echo=True for SQL logs (optional)

def get_db():
    with Session(engine) as session:
        yield session
