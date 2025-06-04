from app.core.base import FHIRService
from app.models.relatedPerson_model import RelatedPersonResource
from app.db.mongo import relatedperson_collection
import uuid



class RelatedPersonService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = relatedperson_collection(data)
        relatedperson_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = relatedperson_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return RelatedPersonResource(data).get_resource()
