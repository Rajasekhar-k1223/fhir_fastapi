from app.core.base import FHIRService
from app.models.doumentReference_model import DocumentReferenceResource
from app.db.mongo import documentReference_collection
import uuid



class DocumentReferenceService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = documentReference_collection(data)
        documentReference_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = documentReference_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return DocumentReferenceResource(data).get_resource()
