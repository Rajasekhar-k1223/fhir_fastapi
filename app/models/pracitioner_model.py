import datetime
from copy import deepcopy
from bson import ObjectId
from typing import Dict, Any

import pytz
from fhir.resources.practitioner import Practitioner as FHIRPractitioner
from fhir.resources.meta import Meta

from app.models.pg_practitioner_model import PGPractitioner  # ✅ Avoid circular import
from app.db.mongo import MongoClient


class PractitionerResource:
    def __init__(self, data: dict, user_id: str, username: str, mobile: str):
        """
        Construct FHIR Practitioner resource and prepare for persistence.

        Args:
            data (dict): Raw FHIR practitioner JSON input.
            user_id (str): Associated user ID.
            username (str): Full name of the practitioner.
            mobile (str): Contact mobile number.
        """
        self.user_id = user_id
        self.username = username
        self.mobile = mobile

        cleaned_data = self._sanitize(data)
        self.practitioner = FHIRPractitioner(**cleaned_data)

        # Set required fields
        self.practitioner.id = str(ObjectId())
        self.practitioner.name = [{"use": "official", "text": username}]
        self.practitioner.telecom = [{"system": "phone", "value": mobile}]
        self.practitioner.identifier = [{
            "use": "official",
            "system": "https://uid.nesthives.com",
            "value": user_id
        }]
        self.practitioner.meta = Meta.construct(
            lastUpdated=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC).isoformat()
        )

    def _sanitize(self, data: dict) -> dict:
        """Remove extra fields and fix nested FHIR substructures."""
        data = deepcopy(data)

        # Remove MongoDB and non-FHIR custom fields
        data.pop("_id", None)
        data.pop("lastUpdated", None)
        data.pop("managingOrganization", None)

        # Clean qualification.date period
        if "qualification" in data:
            for qualification in data["qualification"]:
                period = qualification.get("period", {})
                if "start" in period:
                    period["start"] = self._make_timezone_aware(period["start"])
                if "end" in period:
                    period["end"] = self._make_timezone_aware(period["end"])

        # Clean address extras
        if "address" in data:
            for address in data["address"]:
                address.pop("longitude", None)
                address.pop("latitude", None)
                address.pop("altitude", None)

        return data

    def _make_timezone_aware(self, dt_str: str) -> str:
        """Convert naive datetime string to timezone-aware ISO format."""
        try:
            dt_obj = datetime.datetime.fromisoformat(dt_str)
            if dt_obj.tzinfo is None:
                dt_obj = dt_obj.replace(tzinfo=pytz.UTC)
            return dt_obj.isoformat()
        except Exception:
            return dt_str

    def save_to_postgres(self, db_session) -> PGPractitioner:
        """
        Save practitioner to PostgreSQL via SQLModel.

        Returns:
            PGPractitioner: Persisted SQLModel instance.
        """
        practitioner = PGPractitioner(
            user_id=self.user_id,
            name=self.username,
            mobile=self.mobile
        )
        db_session.add(practitioner)
        db_session.commit()
        db_session.refresh(practitioner)
        return practitioner

    def save_to_mongodb(self):
        """Save practitioner as FHIR JSON to MongoDB."""
        mongo_db = MongoClient()
        return mongo_db["practitioners"].insert_one(self.to_dict()).inserted_id

    def get_resource(self):
        """Return full FHIR resource object."""
        return self.practitioner

    def get_id(self):
        """Return FHIR ID."""
        return self.practitioner.id

    def to_dict(self) -> Dict[str, Any]:
        """Return FHIR resource as dict."""
        return self.practitioner.dict()
