from fastapi import APIRouter,HTTPException,Query
from app.services.procedure_service import ProcedureService

router = APIRouter()
services = ProcedureService()

@router.get("/procedure_getName/{id}")
def get_procedure_name(id:str):
    try:
        procedure = services.get_by_id(id)
        return {"message":"Patient found","data":procedure.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    