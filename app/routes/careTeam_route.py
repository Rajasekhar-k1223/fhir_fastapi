from fastapi import APIRouter,HTTPException,Query
from app.services.careTeam_service import CareTeamService

router = APIRouter()
services = CareTeamService()

@router.get("/careteam_getName/{id}")
def get_careteam_name(id:str):
    try:
        careteam = services.get_by_id(id)
        return {"message":"Patient found","data":careteam.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    