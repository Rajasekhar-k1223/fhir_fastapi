from app.core.base import FHIRService
from app.models.allergyIntolerance_model import AllergyIntoleranceResource
from app.db.mongo import allergies_collection
import uuid



class AllergyIntoleranceService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = allergies_collection(data)
        allergies_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = allergies_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return AllergyIntoleranceResource(data).get_resource()
