from app.core.base import FHIRService
from app.models.careTeam_model import CareTeamResource
from app.db.mongo import careteams_collection
import uuid



class CareTeamService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = careteams_collection(data)
        careteams_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = careteams_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return CareTeamResource(data).get_resource()
