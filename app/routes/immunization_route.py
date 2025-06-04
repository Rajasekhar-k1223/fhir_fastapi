from fastapi import APIRouter,HTTPException,Query
from app.services.immunization_service import ImmunizationService

router = APIRouter()
services = ImmunizationService()

@router.get("/immunization_getName/{id}")
def get_immunization_name(id:str):
    try:
        immunization = services.get_by_id(id)
        return {"message":"Patient found","data":immunization.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    