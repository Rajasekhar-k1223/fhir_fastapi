from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "FHIR FastAPI"
    ENVIRONMENT: str = "development"
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "healthcare_db_new"
    MONGO_PATIENT_COLLECTION: str = "patients"

    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
