from fhir.resources.patient import Patient
from copy import deepcopy

class PatientResource:
    def __init__(self, data: dict):
        cleaned_data = self._sanitize(data)
        self.patient = Patient(**cleaned_data)

    def _sanitize(self, data: dict) -> dict:
        """Remove non-FHIR fields like latitude/longitude/altitude and others."""
        data = deepcopy(data)

        # Clean up address list
        if "address" in data:
            for address in data["address"]:
                address.pop("longitude", None)
                address.pop("latitude", None)
                address.pop("altitude", None)

        # Remove non-FHIR top-level fields
        data.pop("lastUpdated", None)

        return data

    def get_resource(self):
        return self.patient

    def get_id(self):
        return self.patient.id

    def to_dict(self):
        return self.patient.dict()
