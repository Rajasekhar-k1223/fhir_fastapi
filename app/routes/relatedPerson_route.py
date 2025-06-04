from fastapi import APIRouter,HTTPException,Query
from app.services.related_person_service import RelatedPersonService

router = APIRouter()
services = RelatedPersonService()

@router.get("/relatperson_getName/{id}")
def get_relatperson_name(id:str):
    try:
        relatedperson = services.get_by_id(id)
        return {"message":"Patient found","data":relatedperson.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    