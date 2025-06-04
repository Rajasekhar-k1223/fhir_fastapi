from fastapi import APIRouter,HTTPException,Query
from app.services.observation_service import ObservationService

router = APIRouter()
services = ObservationService()

@router.get("/observation_getName/{id}")
def get_observation_name(id:str):
    try:
        observation = services.get_by_id(id)
        return {"message":"Patient found","data":observation.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    