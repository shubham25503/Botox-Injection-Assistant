from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.utils.dependencies import admin_only
from app.database import users_collection
from app.services.admin_user_service import (
    get_all_users, get_user_by_id, update_user, delete_user
)
from app.schemas.admin_user_schema import AdminUserResponse, AdminUserUpdate

router = APIRouter(tags=["Admin Users"])

@router.get("/", response_model=List[AdminUserResponse])
async def list_users(current_user=Depends(admin_only)):
    try:
        return await get_all_users(users_collection)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@router.get("/{user_id}", response_model=AdminUserResponse)
async def get_user(user_id: str, current_user=Depends(admin_only)):
    try:
        user = await get_user_by_id(users_collection, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

@router.put("/{user_id}")
async def update_user_info(user_id: str, update_data: AdminUserUpdate, current_user=Depends(admin_only)):
    try:
        success = await update_user(users_collection, user_id, update_data)
        if not success:
            raise HTTPException(status_code=404, detail="User not found or no update performed")
        return {"message": "User updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

@router.delete("/{user_id}")
async def delete_user_info(user_id: str, current_user=Depends(admin_only)):
    try:
        success = await delete_user(users_collection, user_id, current_user)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")
