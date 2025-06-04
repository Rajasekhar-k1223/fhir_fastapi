from fastapi import APIRouter,HTTPException,Query
from app.services.encounter_service import EncounterService

router = APIRouter()
services = EncounterService()

@router.get("/encounter_getName/{id}")
def get_encounter_name(id:str):
    try:
        encounter = services.get_by_id(id)
        return {"message":"Patient found","data":encounter.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    