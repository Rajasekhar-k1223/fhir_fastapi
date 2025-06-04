from app.core.base import FHIRService
from app.models.encounter_model import EncounterResource
from app.db.mongo import encounters_collection
import uuid



class EncounterService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = encounters_collection(data)
        encounters_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = encounters_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return EncounterResource(data).get_resource()
