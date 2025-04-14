from fastapi import APIRouter, HTTPException, Depends
from app.schemas.procedure_schema import ProcedureCreate, ProcedureEdit, ProcedureOut
from app.services.procedure_services import create_procedure, get_all_procedures, update_procedure, get_procedure, delete_procedure, get_all_procedures_for_user
from app.utils.dependencies import get_current_user, admin_only
from app.utils.functions import create_response, handle_exception
from fastapi import APIRouter, Depends, Form, UploadFile, File
from typing import List
from datetime import datetime

router = APIRouter(tags=["Procedures"])

@router.post("/")
async def add_procedure(
    patient_name: str = Form(...),
    patient_gender: str = Form(...),
    patient_age: int = Form(...),
    institution_name: str = Form(...),
    procedure_date: datetime = Form(...),
    injection_areas: List[str] = Form(...),
    image: UploadFile = File(...),
    is_deleted: bool = Form(False),
    current_user=Depends(get_current_user)
):
    try:
        image_path = f"uploads/{image.filename}"
        with open(image_path, "wb") as f:
            f.write(await image.read())

        procedure_data = {
            "patient_name": patient_name,
            "patient_gender": patient_gender,
            "patient_age": patient_age,
            "institution_name": institution_name,
            "procedure_date": procedure_date,
            "injection_areas": injection_areas,
            "image_path": image_path,
            "is_deleted": is_deleted
        }

        procedure_id = await create_procedure(procedure_data, current_user)
        return create_response(200, True, "", {"procedure_id": procedure_id})

    except Exception as e:
        print("procedures post", e)
        raise HTTPException(status_code=500, detail=handle_exception(e, ""))



@router.get("/",  dependencies=[Depends(admin_only)])
async def list_procedures():
    try:
        return  create_response(200, True,"",await get_all_procedures())
    except Exception as e:
        print("procedures get", e)
        raise HTTPException(status_code=500, detail=handle_exception(e,"",500))
    




# @router.get("/detail/{procedure_id}", response_model=ProcedureOut)
@router.get("/detail/{procedure_id}")
async def list_procedures(procedure_id: str,  current_user= Depends(get_current_user)):
    try:
        return  create_response(200, True,"",await get_procedure(procedure_id))
    except Exception as e:
        print("procedures get", e)
        raise HTTPException(status_code=500, detail=handle_exception(e,"",500))
     
# PUT: https://localhost:8080/procudure/id -> request body {} 

@router.get("/all/{user_id}", dependencies=[Depends(get_current_user)])
async def list_procedures(user_id:str):
    try:
        return  create_response(200, True,"",await get_all_procedures_for_user(user_id))
    except Exception as e:
        print("procedures get", e)
        raise HTTPException(status_code=500, detail=handle_exception(e,"",500))


@router.put("/{procedure_id}",   dependencies=[Depends(get_current_user)])
async def edit_procedures(procedure_id:str,data: ProcedureEdit):
    try:
        updated=await update_procedure(procedure_id,data)
        if updated:
            return  create_response(200, True,"",{"status":"Update Successful"})
    except Exception as e:
        print("procedures put", e)
        raise HTTPException(status_code=500, detail=handle_exception(e,"",500))

@router.delete("/{procedure_id}", dependencies=[Depends(get_current_user)])
async def delete_procedures(procedure_id:str):
    try:
        deleted=await delete_procedure(procedure_id)
        if deleted:
            return  create_response(200, True,"",{"status":"Deleted Successful"})
    except Exception as e:
        print("procedures delete", e)
        raise HTTPException(status_code=500,detail=handle_exception(e,"",500))

