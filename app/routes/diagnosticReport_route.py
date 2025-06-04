from fastapi import APIRouter,HTTPException,Query
from app.services.diagnostic_report_service import DiagnosticReportService

router = APIRouter()
services = DiagnosticReportService()

@router.get("/diagnostic_getName/{id}")
def get_diagnostic_name(id:str):
    try:
        diagnosticreport = services.get_by_id(id)
        return {"message":"Patient found","data":diagnosticreport.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    