from app.core.base import FHIRService
from app.models.coverage_model import CoverageResource
from app.db.mongo import coverage_collection
import uuid



class CoverageService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = coverage_collection(data)
        coverage_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = coverage_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return CoverageResource(data).get_resource()
