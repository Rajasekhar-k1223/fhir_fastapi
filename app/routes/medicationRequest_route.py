from fastapi import APIRouter,HTTPException,Query
from app.services.medical_request_service import MedicationRequestService

router = APIRouter()
services = MedicationRequestService()

@router.get("/medicationreq_getName/{id}")
def get_medicationreq_name(id:str):
    try:
        medirequest = services.get_by_id(id)
        return {"message":"Patient found","data":medirequest.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    