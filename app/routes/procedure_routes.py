from fastapi import APIRouter, HTTPException, Depends
from app.schemas.procedure_schema import ProcedureCreate, ProcedureEdit, ProcedureOut
from app.services.procedure_services import edit_image_procedure, create_procedure, get_all_procedures, get_procedure, delete_procedure, get_all_procedures_for_user
from app.utils.dependencies import get_current_user, admin_only
from app.utils.functions import create_response, handle_exception
from fastapi import APIRouter, Depends, Form, UploadFile, File
from typing import List
from typing import Optional
from datetime import datetime
from app.database import procedure_collection
from bson import ObjectId
import os

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
        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.dirname(current_dir))
        new_current_dir = os.getcwd()
        patient_dir = os.path.join(new_current_dir, f"uploads/{patient_name}")
        os.makedirs(patient_dir, exist_ok=True)
        image_path = os.path.join(patient_dir, f"dose_0.jpg")
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

        procedure = await create_procedure(procedure_data, current_user)
        procedure["procedure_id"]=procedure["_id"]
        return create_response(200, True, "", procedure)

    except Exception as e:
        print("procedures post", e)
        raise HTTPException(status_code=500, detail=handle_exception(e, ""))



@router.get("/",  dependencies=[Depends(admin_only)])
async def list_procedures():
    try:
        data=await get_all_procedures()
        return  create_response(200, True,"",data)
    except Exception as e:
        print("procedures get", e)
        raise HTTPException(status_code=500, detail=handle_exception(e,"",500))
    




# @router.get("/detail/{procedure_id}", response_model=ProcedureOut)
@router.get("/detail/{procedure_id}")
async def list_procedures(procedure_id: str,  current_user= Depends(get_current_user)):
    try:
        data=await get_procedure(procedure_id)
        return  create_response(200, True,"",data)
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

@router.put("/change-image/{procedure_id}", dependencies=[Depends(get_current_user)])
async def edit_image(
    procedure_id: str,
    image: UploadFile = File(...)
    ):
    try:
        return create_response(200, True, "Image updated successfully", await edit_image_procedure(procedure_id,image))
    except Exception as e :
        print("edit_image error:", e)
        raise HTTPException(status_code=500, detail=handle_exception(e, ""))

@router.put("/{procedure_id}", dependencies=[Depends(get_current_user)])
async def edit_procedure(
    procedure_id: str,
    patient_name: Optional[str] = Form(None),
    patient_gender: Optional[str] = Form(None),
    patient_age: Optional[int] = Form(None),
    institution_name: Optional[str] = Form(None),
    procedure_date: Optional[datetime] = Form(None),
    injection_areas: Optional[List[str]] = Form(None)
):
    try:
        update_data = {}
        if patient_name is not None:
            update_data["patient_name"] = patient_name
        if patient_gender is not None:
            update_data["patient_gender"] = patient_gender
        if patient_age is not None:
            update_data["patient_age"] = patient_age
        if institution_name is not None:
            update_data["institution_name"] = institution_name
        if procedure_date is not None:
            update_data["procedure_date"] = datetime.combine(procedure_date, datetime.min.time())
        if injection_areas is not None:
            update_data["injection_areas"] = injection_areas

        if not update_data:
            raise ValueError("No fields provided for update.")

        result = await procedure_collection.update_one(
            {"_id": ObjectId(procedure_id)},
            {"$set": update_data}
        )

        if result.matched_count == 0:
            raise ValueError("No procedure found with the given ID.")

        return create_response(200, True, "Update Successful", {"status": "Update Successful"})

    except Exception as e:
        print("procedures put", e)
        raise HTTPException(status_code=500, detail=handle_exception(e, ""))
    

@router.delete("/{procedure_id}", dependencies=[Depends(get_current_user)])
async def delete_procedures(procedure_id:str):
    try:
        deleted=await delete_procedure(procedure_id)
        if deleted:
            return  create_response(200, True,"",{"status":"Deleted Successful"})
    except Exception as e:
        print("procedures delete", e)
        raise HTTPException(status_code=500,detail=handle_exception(e,"",500))

