from fhir.resources.relatedperson import RelatedPerson
from copy import deepcopy
from datetime import datetime
import pytz


class RelatedPersonResource:
    def __init__(self, data: dict):
        cleaned_data = self._sanitize(data)
        self.relatedperson = RelatedPerson(**cleaned_data)

    def _sanitize(self, data: dict) -> dict:
        """Clean input data for FHIR Practitioner model."""
        data = deepcopy(data)

        # Remove MongoDB _id field
        data.pop("_id", None)

        # Remove non-FHIR fields
        data.pop("lastUpdated", None)
        data.pop("managingOrganization", None)

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
        return self.relatedperson

    def get_id(self):
        return self.relatedperson.id

    def to_dict(self):
        return self.relatedperson.dict()
