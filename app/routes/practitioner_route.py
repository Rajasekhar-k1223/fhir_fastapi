from fastapi import APIRouter,HTTPException,Query
from app.services.pracitioner_service import PractitionerService

router = APIRouter()
services = PractitionerService()

@router.get("/practitioner_getName/{id}")
def get_practioner_name(id:str):
    try:
        pracitioner = services.get_by_id(id)
        return {"message":"Patient found","data":pracitioner}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    