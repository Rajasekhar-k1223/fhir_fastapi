from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "FHIR FastAPI"
    ENVIRONMENT: str = "development"
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "healthcare_db_new"
    MONGO_PATIENT_COLLECTION: str = "patients"
    MONGO_PRACTITIONER_COLLECTION:str = "practitioners"
    MONGO_ORGANIZATION_COLLECTION:str = "organizations"
    MONGO_LOCATIONS_COLLECTION:str = "locations"
    MONGO_APPOINTMENT_COLLECTION:str = "appointments"
    MONGO_CONDITIONS_COLLECTION:str = "conditions"
    MONGO_COVERAGE_COLLECTION:str = "coverages"
    MONGO_DOCUMENTREFERENCE_COLLECTION:str = "document_references"
    MONGO_ENCOUNTERS_COLLECTION:str = "encounters"
    MONGO_EPISODEOFCARE_COLLECTION:str = "episodeofcares"
    MONGO_OBSERVATIONS_COLLECTION:str = "observations"
    MONGO_MEDICATION_REQUESTS_COLLECTION:str = "medication_requests"
    MONGO_ENDPOINTS_COLLECTION:str = "endpoints"
    MONGO_DIAGNOSTIC_REPORTS_COLLECTION:str = "diagnostic_reports"
    MONGO_IMMUNIZATION_COLLECTION:str = "immunizations"
    MONGO_SPECIMENS_COLLECTION:str = "specimens"
    MONGO_MEDICATIONS_COLLECTION:str = "medications"
    MONGO_INSURANCE_COLLECTION:str = "insurance"
    MONGO_CARETEAMS_COLLECTION:str = "careteams"
    MONGO_HEALTHCARE_SERVICES_COLLECTION:str = "healthcare_services"
    MONGO_GOALS_COLLECTION:str = "goals"
    MONGO_CAREPLANS_COLLECTION:str = "careplans"
    MONGO_ALLERGY_INTOLERANCES_COLLECTION:str = "allergy_intolerances"
    MONGO_DEVICES_COLLECTION:str = "devices"
    MONGO_PROCEDURE_COLLECTION:str = "procedures"
    MONGO_RELATED_PERSON_COLLECTION:str = "related_persons"
    FAST2SMS_API_KEY: str 
    
    model_config = ConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
