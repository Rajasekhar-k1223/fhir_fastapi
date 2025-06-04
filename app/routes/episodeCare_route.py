from fastapi import APIRouter,HTTPException,Query
from app.services.episodeCare_service import EpisodeOfCareService

router = APIRouter()
services = EpisodeOfCareService()

@router.get("/episodecare_getName/{id}")
def get_episodecare_name(id:str):
    try:
        episodecare = services.get_by_id(id)
        return {"message":"Patient found","data":episodecare.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    