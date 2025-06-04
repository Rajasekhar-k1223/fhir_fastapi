from fastapi import APIRouter,HTTPException,Query
from app.services.condition_service import ConditionService

router = APIRouter()
services = ConditionService()

@router.get("/condition_getName/{id}")
def get_condition_name(id:str):
    try:
        condition = services.get_by_id(id)
        return {"message":"Patient found","data":condition.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    