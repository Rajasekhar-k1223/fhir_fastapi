from app.core.base import FHIRService
from app.models.observation_model import ObservationResource
from app.db.mongo import observations_collection
import uuid



class ObservationService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = observations_collection(data)
        observations_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = observations_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return ObservationResource(data).get_resource()
