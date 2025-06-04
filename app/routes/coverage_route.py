from fastapi import APIRouter,HTTPException,Query
from app.services.coverage_service import CoverageService

router = APIRouter()
services = CoverageService()

@router.get("/coverage_getName/{id}")
def get_coverage_name(id:str):
    try:
        coverage = services.get_by_id(id)
        return {"message":"Patient found","data":coverage.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    