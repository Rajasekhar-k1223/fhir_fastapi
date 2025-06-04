from fhir.resources.practitioner import Practitioner
from copy import deepcopy
from datetime import datetime
import pytz


class PractitionerResource:
    def __init__(self, data: dict):
        cleaned_data = self._sanitize(data)
        self.practitioner = Practitioner(**cleaned_data)

    def _sanitize(self, data: dict) -> dict:
        """Clean input data for FHIR Practitioner model."""
        data = deepcopy(data)

        # Remove MongoDB _id field
        data.pop("_id", None)

        # Remove non-FHIR fields
        data.pop("lastUpdated", None)
        data.pop("managingOrganization", None)

        # Clean up qualification datetime fields
        if "qualification" in data:
            for qualification in data["qualification"]:
                period = qualification.get("period")
                if period:
                    if "start" in period:
                        period["start"] = self._make_timezone_aware(period["start"])
                    if "end" in period:
                        period["end"] = self._make_timezone_aware(period["end"])

        # Clean address fields if they exist
        if "address" in data:
            for address in data["address"]:
                address.pop("longitude", None)
                address.pop("latitude", None)
                address.pop("altitude", None)

        return data

    def _make_timezone_aware(self, dt_str: str) -> str:
        """Ensure the datetime string is timezone-aware (UTC)."""
        try:
            dt_obj = datetime.fromisoformat(dt_str)
            if dt_obj.tzinfo is None:
                dt_obj = dt_obj.replace(tzinfo=pytz.UTC)
            return dt_obj.isoformat()
        except Exception:
            return dt_str  # fallback in case of invalid date format

    def get_resource(self):
        return self.practitioner

    def get_id(self):
        return self.practitioner.id

    def to_dict(self):
        return self.practitioner.dict()
