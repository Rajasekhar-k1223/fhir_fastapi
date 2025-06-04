from app.core.base import FHIRService
from app.models.procedure_model import ProcedureResource
from app.db.mongo import procedure_collection
import uuid



class ProcedureService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = procedure_collection(data)
        procedure_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = procedure_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return ProcedureResource(data).get_resource()
