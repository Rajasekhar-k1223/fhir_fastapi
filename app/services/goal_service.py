from app.core.base import FHIRService
from app.models.goal_model import GoalResource
from app.db.mongo import goals_collection
import uuid



class GoalService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = goals_collection(data)
        goals_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = goals_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return GoalResource(data).get_resource()
