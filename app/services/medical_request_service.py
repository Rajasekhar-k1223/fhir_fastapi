from app.core.base import FHIRService
from app.models.medicationRequest_mode import MedicationRequestResource
from app.db.mongo import medication_requests_collection
import uuid



class MedicationRequestService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = medication_requests_collection(data)
        medication_requests_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = medication_requests_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return MedicationRequestResource(data).get_resource()
