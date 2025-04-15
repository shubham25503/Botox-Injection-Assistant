from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.utils.dependencies import admin_only
from app.database import users_collection
from app.services.admin_user_service import (
    get_all_users, get_user_by_id, update_user, delete_user
)
from app.schemas.admin_user_schema import AdminUserResponse, AdminUserUpdate
from app.utils.functions import create_response, handle_exception

router = APIRouter(tags=["Admin Users"])

@router.get("/")
async def list_users(current_user=Depends(admin_only)):
    try:
        return create_response(200, True, "", await get_all_users(users_collection))
    except Exception as e:
        raise HTTPException(status_code=500,detail=handle_exception(e,f"Failed to fetch users: {str(e)}",500) )

@router.get("/{user_id}", response_model=AdminUserResponse)
async def get_user(user_id: str, current_user=Depends(admin_only)):
    try:
        user = await get_user_by_id(users_collection, user_id)
        if not user:
            raise HTTPException(status_code=404, detail=handle_exception(None,"User not found",404))
        return create_response(200, True, "", user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=handle_exception(e,f"Failed to fetch user: {str(e)}",500))

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
