from fastapi import APIRouter,HTTPException,Query
from app.services.allergyIntolerance_serve import AllergyIntoleranceService

router = APIRouter()
services = AllergyIntoleranceService()

@router.get("/allergy_getName/{id}")
def get_allery_name(id:str):
    try:
        allergyIntolerance = services.get_by_id(id)
        return {"message":"Patient found","data":allergyIntolerance.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    