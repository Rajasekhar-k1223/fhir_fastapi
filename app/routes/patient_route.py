from fastapi import APIRouter,HTTPException,Query,Depends
from app.services.patient_service import PatientService
from app.auth.jwt_handler import get_current_user
router = APIRouter()
service = PatientService()

@router.post("/patient")
def create_patient(data:dict):
    try:
        patient = service.create(data)
        return {"message":"Patient created","data":patient.dict()}
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.get("/patients")
def get_all_patients(skip:int=Query(0,ge=0),limit:int=Query(100,ge=1,le=1000)):
    try:
        patients= service.get_all(skip=skip,limit=limit)
        return {"message":"Patients retrieved","total":patients["total"],"count":patients["count"],"data":patients["data"]}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))

@router.get("/patient/{patient_id}")
def get_patient(patient_id:str,token_data: dict = Depends(get_current_user)):
    try:
        patient = service.get_by_id(patient_id)
        return {"message":"Patient found","data":patient}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    
    