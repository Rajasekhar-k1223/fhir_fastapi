from app.core.base import FHIRService
from app.models.organization_model import OrganizationResource
from app.db.mongo import organization_collection
import uuid



class OganizationService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = organization_collection(data)
        organization_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        print(id)
        data = organization_collection.find_one({"_id":id},{"_id":0,"name":1})
        # print(data)
        if not data:
            raise ValueError("Organization not found")
        return OrganizationResource(data).get_resource()
