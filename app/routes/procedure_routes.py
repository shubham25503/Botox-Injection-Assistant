from fastapi import APIRouter, HTTPException, Depends
from app.schemas.procedure_schema import ProcedureCreate, ProcedureEdit
from app.services.procedure_services import create_procedure, get_all_procedures, update_procedure, delete_procedure
from app.utils.dependencies import get_current_user

router = APIRouter(tags=["Procedures"])

@router.post("/", dependencies=[Depends(get_current_user)])
async def add_procedure(procedure: ProcedureCreate):
    try:
        procedure_id = await create_procedure(procedure)
        return {"status": "success", "procedure_id": procedure_id}
    except Exception as e:
        print("procedures post", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/",  dependencies=[Depends(get_current_user)])
async def list_procedures():
    try:
        return await get_all_procedures()
    except Exception as e:
        print("procedures get", e)
        raise HTTPException(status_code=500, detail=str(e))
    
# PUT: https://localhost:8080/procudure/id -> request body {} 
    
@router.put("/{procedure_id}",   dependencies=[Depends(get_current_user)])
async def edit_procedures(procedure_id:str,data: ProcedureEdit):
    try:
        updated=await update_procedure(procedure_id,data)
        if updated:
            return {"status":"Update Successful"}
    except Exception as e:
        print("procedures put", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{procedure_id}", dependencies=[Depends(get_current_user)])
async def delete_procedures(procedure_id:str):
    try:
        deleted=await delete_procedure(procedure_id)
        if deleted:
            return {"status":"Deleted Successful"}
    except Exception as e:
        print("procedures delete", e)
        raise HTTPException(status_code=500, detail=str(e))
