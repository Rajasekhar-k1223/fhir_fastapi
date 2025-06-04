from fastapi import APIRouter,HTTPException,Query
from app.services.organization_service import OganizationService

router = APIRouter()
services = OganizationService()

@router.get("/organization_getName/{id}")
def get_organization_name(id:str):
    print(id)
    try:
        organization = services.get_by_id(id)
        return {"message":"Organization found","data":organization.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    