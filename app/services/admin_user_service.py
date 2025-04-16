from typing import List, Optional
from bson import ObjectId, errors
from app.schemas.admin_user_schema import AdminUserResponse, AdminUserUpdate
from fastapi import HTTPException
from app.models.user import User
from app.schemas.user_schema import UserSignup
from app.utils.jwt_handler import create_jwt_token
from passlib.context import CryptContext
from app.database import users_collection, procedure_collection
from datetime import datetime

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



async def get_all_users(users_collection):
    try:
        users = []
        async for user in users_collection.find({}):
            user["_id"] = str(user["_id"])
            users.append({**user})
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {str(e)}")

async def get_user_by_id(users_collection, user_id: str) :
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            return {**user}
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
        if str(current_user["_id"])==str(user_id):
            raise HTTPException(status_code=400, detail="You can't Delete yourself")
    
        result = await users_collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0
    except errors.InvalidId:
        raise HTTPException(status_code=400, detail="Invalid user ID format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")

async def create_user(users_collection, user_data:UserSignup, is_admin=False, payment_status=None):
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="User already Exists")
    hashed_pw = hash_password(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pw,
        is_admin=is_admin,
        # access_expires=access_expires,
        # access_code=access_code,
    )
    await users_collection.insert_one(user.dict())
    token = create_jwt_token({
        "email": user.email,
        "is_admin":user.is_admin
        })
    existing_user = await users_collection.find_one({"email": user_data.email})
    existing_user["_id"]=str(existing_user["_id"])

    return {**existing_user}

async def create_procedure(user_id:str, procedure_data: dict):
    # current_user = await users_collection.find_one({"_id": ObjectId(user_id)})
    # procedure_data["doctor_id"] = current_user["_id"]
    procedure_data["doctor_id"] = user_id

    if isinstance(procedure_data["procedure_date"], datetime):
        pass
    else:
        procedure_data["procedure_date"] = datetime.combine(procedure_data["procedure_date"], datetime.min.time())
    
    result = await procedure_collection.insert_one(procedure_data)
    data =await procedure_collection.find_one({"_id":result.inserted_id})
    data["_id"]=str(data["_id"])
    data["doctor_id"]=str(data["doctor_id"])
    return data



def hash_password(password: str) -> str:
    return pwd_context.hash(password)

