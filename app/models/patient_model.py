import datetime
from copy import deepcopy
from bson import ObjectId
from typing import Dict, Any, Optional

from fhir.resources.patient import Patient as FHIRPatient
from fhir.resources.meta import Meta

from app.models.pg_patient_model import PGPatient
from app.db.mongo import patient_collection


class PatientResource:
    def __init__(
        self,
        data: dict,
        user_id: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        mobile: Optional[str] = None,
        aadhar_number: Optional[str] = None
    ):
        """
        Initialize a FHIR-compliant PatientResource object.

        If any key patient information is missing, it defaults to 'unknown'.
        """
        self.user_id = user_id or "unknown"
        self.username = username or "unknown"
        self.email = email or "unknown"
        self.mobile = mobile or "unknown"
        self.aadhar_number = aadhar_number or "unknown"

        cleaned_data = self._sanitize(data)
        self.patient = FHIRPatient(**cleaned_data)

        # Add/override standard fields
        self.patient.id = str(ObjectId())
        self.patient.active = True
        self.patient.name = [{"use": "official", "text": self.username}]
        self.patient.telecom = [{"system": "phone", "value": self.mobile}]
        self.patient.identifier = [{
            "use": "official",
            "system": "https://uid.nesthives.com",
            "value": self.user_id
        }]
        self.patient.meta = Meta.construct(lastUpdated=datetime.datetime.utcnow().isoformat())

        # Set gender and birthDate defaults if missing
        if not self.patient.gender:
            self.patient.gender = "unknown"
        if not self.patient.birthDate:
            self.patient.birthDate = "1990-01-01"
        elif isinstance(self.patient.birthDate, (datetime.date, datetime.datetime)):
            self.patient.birthDate = self.patient.birthDate.isoformat()[:10]
        elif not isinstance(self.patient.birthDate, str):
            self.patient.birthDate = str(self.patient.birthDate)

    def _sanitize(self, data: dict) -> dict:
        """
        Remove non-FHIR fields from the input data.
        """
        data = deepcopy(data)

        if "address" in data:
            for address in data["address"]:
                address.pop("longitude", None)
                address.pop("latitude", None)
                address.pop("altitude", None)

        data.pop("lastUpdated", None)
        return data

    def save_to_postgres(self, db_session) -> PGPatient:
        """
        Save patient metadata to PostgreSQL.
        """
        patient = PGPatient(
            user_id=self.user_id,
            username=self.username,
            email=self.email,
            mobile=self.mobile,
            aadhar_number=self.aadhar_number
        )
        db_session.add(patient)
        db_session.commit()
        db_session.refresh(patient)
        return patient

    def save_to_mongodb(self):
        """
        Save full FHIR-compliant patient resource to MongoDB.
        """
        return patient_collection.insert_one(self.to_dict()).inserted_id

    def get_resource(self):
        """
        Get the FHIR Patient resource object.
        """
        return self.patient

    def get_id(self):
        """
        Get the internal FHIR patient resource ID.
        """
        return self.patient.id

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert FHIR patient resource to a dictionary, sanitizing incompatible types.
        """
        data = self.patient.dict()

        if isinstance(data.get("birthDate"), (datetime.date, datetime.datetime)):
            data["birthDate"] = data["birthDate"].isoformat()[:10]

        data.pop("_id", None)
        return data
