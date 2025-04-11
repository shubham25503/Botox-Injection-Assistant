from typing import List, Optional
from bson import ObjectId, errors
from app.schemas.admin_user_schema import AdminUserResponse, AdminUserUpdate
from fastapi import HTTPException

async def get_all_users(users_collection) -> List[AdminUserResponse]:
    try:
        users = []
        async for user in users_collection.find({}):
            user["id"] = str(user["_id"])
            users.append(AdminUserResponse(**user))
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

async def get_user_by_id(users_collection, user_id: str) -> Optional[AdminUserResponse]:
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["id"] = str(user["_id"])
            return AdminUserResponse(**user)
        return None
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {str(e)}")

async def update_user(users_collection, user_id: str, update_data: AdminUserUpdate):
    try:
        result = await users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data.dict(exclude_unset=True)}
        )
        return result.modified_count > 0
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

async def delete_user(users_collection, user_id: str, current_user):
    try:
        result = await users_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
