from app.core.base import FHIRService
from app.models.appointment_model import AppointmentResource
from app.db.mongo import appointment_collection
import uuid



class AppointmentService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = appointment_collection(data)
        practitioappointment_collectionner_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = appointment_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return AppointmentResource(data).get_resource()
