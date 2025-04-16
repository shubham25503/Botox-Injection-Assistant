from fastapi import APIRouter, Depends, HTTPException, Form,status, UploadFile, File
from typing import List, Optional
from app.utils.dependencies import admin_only
from app.schemas.user_schema import UserSignup
from bson import ObjectId
from datetime import datetime
from app.database import users_collection
from app.services.admin_user_service import (
    get_all_users, get_user_by_id, update_user, delete_user, create_user, create_procedure
)
from app.schemas.admin_user_schema import AdminUserResponse, AdminUserUpdate
from app.utils.functions import create_response, handle_exception
import os 

router = APIRouter(tags=["Admin Users"])

@router.get("/")
async def list_users(current_user=Depends(admin_only)):
    try:
        return create_response(200, True, "", await get_all_users(users_collection))
    except Exception as e:
        raise HTTPException(status_code=500,detail=handle_exception(e,f"Failed to fetch users: {str(e)}",500) )

@router.get("/{user_id}")
async def get_user(user_id: str, current_user=Depends(admin_only)):
    try:
        user = await get_user_by_id(users_collection, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=handle_exception(None,"User not found",404))
        return create_response(200, True, "", user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=handle_exception(e,f"Failed to fetch user: {str(e)}",500))

@router.post("/")
async def create_user_admin(user: UserSignup, current_user=Depends(admin_only)):
    try:
        # print(user)
        new_user = await create_user(users_collection, user)
        return create_response(200,True,"User Created Successfully",new_user)
    except Exception as e:
        print("signup",e)
        raise HTTPException(status_code=400, detail=handle_exception(e, "Error creating user"))

@router.post("/procedure/{user_id}")
async def create_procedure_admin(user_id:str,
    patient_name: str = Form(...),
    patient_gender: str = Form(...),
    patient_age: int = Form(...),
    patient_notes:str=Form(...),
    institution_name: str = Form(...),
    procedure_date: datetime = Form(...),
    injection_areas: str = Form(...),
    image: UploadFile = File(...),
    is_deleted: bool = Form(False), current_user=Depends(admin_only)):

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
            "patient_notes":patient_notes,
            "institution_name": institution_name,
            "procedure_date": procedure_date,
            "injection_areas": injection_areas,
            "image_path": image_path,
            "is_deleted": is_deleted
        }

        new_user = await create_procedure(user_id,procedure_data)
        return create_response(200,True,"User Created Successfully",new_user)
    except Exception as e:
        print("signup",e)
        raise HTTPException(status_code=400, detail=handle_exception(e, "Error creating user"))




@router.put("/{user_id}")
async def update_user_info(user_id: str, update_data: AdminUserUpdate, current_user=Depends(admin_only)):
    try:
        success = await update_user(users_collection, user_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail=handle_exception(None,"User not found or no update performed",404))
        return create_response(200, True,  "User updated successfully",None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=handle_exception(e,f"Failed to update user: {str(e)}",500))

@router.delete("/{user_id}")
async def delete_user_info(user_id: str, current_user=Depends(admin_only)):
    try:
        success = await delete_user(users_collection, user_id, current_user)
        if not success:
            raise HTTPException(status_code=404, detail=handle_exception(None,"User not found",404))
        return create_response(200, True, "User deleted successfully", None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=handle_exception(e,f"Failed to delete user: {str(e)}",500))
