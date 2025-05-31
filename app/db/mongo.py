from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGO_URI)
db=client[settings.MONGO_DB]
patient_collection = db[settings.MONGO_PATIENT_COLLECTION]