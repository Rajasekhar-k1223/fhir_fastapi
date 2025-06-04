from fastapi import APIRouter,HTTPException,Query
from app.services.appointment_service import AppointmentService

router = APIRouter()
services = AppointmentService()

@router.get("/appointment_getName/{id}")
def get_appointment_name(id:str):
    try:
        appointment = services.get_by_id(id)
        return {"message":"Patient found","data":appointment.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    