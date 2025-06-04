from fastapi import APIRouter,HTTPException,Query
from app.services.document_reference_service import DocumentReferenceService

router = APIRouter()
services = DocumentReferenceService()

@router.get("/document_getName/{id}")
def get_document_name(id:str):
    try:
        docreference = services.get_by_id(id)
        return {"message":"Patient found","data":docreference.dict()}
    except Exception as e:
        raise HTTPException(status_code=404,detail=str(e))
    