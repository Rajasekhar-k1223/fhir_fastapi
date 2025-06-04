from app.core.base import FHIRService
from app.models.immunization_model import ImmunizationResource
from app.db.mongo import immunization_collection
import uuid



class ImmunizationService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = immunization_collection(data)
        immunization_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = immunization_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return ImmunizationResource(data).get_resource()
