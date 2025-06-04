from app.core.base import FHIRService
from app.models.carePlan_model import CarePlanResource
from app.db.mongo import careplans_collection
import uuid



class CarePlanService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = careplans_collection(data)
        careplans_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = careplans_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return CarePlanResource(data).get_resource()
