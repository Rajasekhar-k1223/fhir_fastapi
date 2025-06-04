from app.core.base import FHIRService
from app.models.diagnosticReport_model import DiagnosticReportResource
from app.db.mongo import diagnostic_reports_collection
import uuid



class DiagnosticReportService(FHIRService):
    def create(self, data:dict):
        if "id" not in data:
            data["id"] = str(uuid.uuid4())
        practitioner = diagnostic_reports_collection(data)
        diagnostic_reports_collection.insert_one(practitioner.to_dict())
        return practitioner.get_resource()
    
    def get_by_id(self, id:str):
        data = diagnostic_reports_collection.find_one({"_id":id},{"_id": 0, "name": 1})
        if not data:
            raise ValueError("Patient not found")
        return DiagnosticReportResource(data).get_resource()
