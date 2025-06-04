from app.core.base import FHIRService
from app.models.condition_model import ConditionResource
from app.db.mongo import conditions_collection
import uuid



class ConditionService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = conditions_collection(data)
        conditions_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = conditions_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return ConditionResource(data).get_resource()
