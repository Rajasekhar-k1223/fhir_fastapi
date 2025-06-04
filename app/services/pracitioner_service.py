from app.core.base import FHIRService
from app.models.pracitioner_model import PractitionerResource
from app.db.mongo import practitioner_collection
import uuid



class PractitionerService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = practitioner_collection(data)
        practitioner_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = practitioner_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return PractitionerResource(data).get_resource()
