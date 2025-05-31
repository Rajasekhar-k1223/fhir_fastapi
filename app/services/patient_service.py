from app.core.base import FHIRService
from app.models.patient_model import PatientResource
from app.db.mongo import patient_collection
import uuid

class PatientService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        patient = PatientResource(data)
        patient_collection.insert_one(patient.to_dict())
        return patient.get_resource()
    
    def get_by_id(self, resource_id:str):
        data = patient_collection.find_one({"identifier.value":resource_id},{"_id":0})
        if not data:
            raise ValueError("Patient not found")
        return PatientResource(data).get_resource()
    @staticmethod
    def get_all(skip: int=0,limit:int=1000):
        cursor = patient_collection.find({},{"_id":0}).skip(skip).limit(limit)
        patients = []
        for data in cursor:
            try:
                patient = PatientResource(data)
                patients.append(patient.to_dict())
            except Exception as e:
                print(f"Error parsing patient:{e}")
                continue
            total = patient_collection.count_documents({})
        return {"total":total,"count":len(patients),"data":patients}