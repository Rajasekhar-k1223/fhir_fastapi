from app.core.base import FHIRService
from app.models.episodeCare_model import EpisodeOfCareResource
from app.db.mongo import episodeofcare_collection
import uuid



class EpisodeOfCareService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = episodeofcare_collection(data)
        episodeofcare_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = episodeofcare_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return EpisodeOfCareResource(data).get_resource()
