from fastapi import APIRouter,HTTPException,Query
from app.services.carePlan_service import CarePlanService

router = APIRouter()
services = CarePlanService()

@router.get("/careplan_getName/{id}")
def get_careplan_name(id:str):
    try:
        carePlan = services.get_by_id(id)
        return {"message":"Patient found","data":carePlan.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    