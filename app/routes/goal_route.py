from fastapi import APIRouter,HTTPException,Query
from app.services.goal_service import GoalService

router = APIRouter()
services = GoalService()

@router.get("/goal_getName/{id}")
def get_goal_name(id:str):
    try:
        goal = services.get_by_id(id)
        return {"message":"Patient found","data":goal.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    