import datetime
from copy import deepcopy
from bson import ObjectId
from typing import Dict, Any

from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.meta import Meta

from app.models.pg_patient_model import PGPatient 
from app.db.mongo import patient_collection


class PatientResource:
    def __init__(self, data: dict, user_id: str, username: str, mobile: str, aadhar_number: str):
        self.user_id = user_id
        self.username = username
        self.mobile = mobile
        self.aadhar_number = aadhar_number

        # Clean and initialize FHIR data
        cleaned_data = self._sanitize(data)
        self.patient = FHIRPatient(**cleaned_data)

        # Add/override standard fields
        self.patient.id = str(ObjectId())
        self.patient.active = True
        self.patient.name = [{"use": "official", "text": username}]
        self.patient.telecom = [{"system": "phone", "value": mobile}]
        self.patient.identifier = [{
            "use": "official",
            "system": "https://uid.nesthives.com",
            "value": user_id
        }]
        self.patient.meta = Meta.construct(lastUpdated=datetime.datetime.utcnow().isoformat())

        if not self.patient.gender:
            self.patient.gender = "unknown"
        if not self.patient.birthDate:
            self.patient.birthDate = "1990-01-01"
        elif isinstance(self.patient.birthDate, (datetime.date, datetime.datetime)):
            self.patient.birthDate = self.patient.birthDate.isoformat()[:10]
        elif not isinstance(self.patient.birthDate, str):
            self.patient.birthDate = str(self.patient.birthDate)

    def _sanitize(self, data: dict) -> dict:
        """Remove non-FHIR fields like latitude/longitude/altitude and others."""
        data = deepcopy(data)

        if "address" in data:
            for address in data["address"]:
                address.pop("longitude", None)
                address.pop("latitude", None)
                address.pop("altitude", None)

        data.pop("lastUpdated", None)
        return data

    def save_to_postgres(self, db_session) -> PGPatient:
        patient = PGPatient(
            user_id=self.user_id,
            username=self.username,
            mobile=self.mobile,
            aadhar_number=self.aadhar_number
        )
        db_session.add(patient)
        db_session.commit()
        db_session.refresh(patient)
        return patient

    def save_to_mongodb(self):
        return patient_collection.insert_one(self.to_dict()).inserted_id

    def get_resource(self):
        return self.patient

    def get_id(self):
        return self.patient.id

    def to_dict(self) -> Dict[str, Any]:
        """Convert FHIR patient resource to dict and clean incompatible types."""
        data = self.patient.dict()

        # Ensure birthDate is a string
        if isinstance(data.get("birthDate"), (datetime.date, datetime.datetime)):
            data["birthDate"] = data["birthDate"].isoformat()[:10]

        # Remove or stringify ObjectId
        data.pop("_id", None)

        return data
