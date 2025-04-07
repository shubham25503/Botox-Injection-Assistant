from passlib.context import CryptContext
# from app.models.user import users_collection
from app.models.user import User
from app.schemas.user_schema import UserSignup, UserEdit
from datetime import datetime, timedelta
from app.utils.jwt_handler import create_jwt_token
from app.database import db
import uuid


users_collection = db["users"]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

plan_durations = {
    "monthly": 30,
    "semiannual": 182,
    "annual": 365,
}

async def create_user(user_data: UserSignup, is_admin=False):
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise Exception("User already exists")

    hashed_pw = hash_password(user_data.password)
    access_days = plan_durations.get(user_data.plan.lower(), 0)
    access_expires = datetime.now() + timedelta(days=access_days)
    access_code = str(uuid.uuid4())
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pw,
        is_admin=is_admin,
        access_expires=access_expires,
        access_code=access_code,
    )
    print(user.dict())
    await users_collection.insert_one(user.dict())
    return  user


async def update_user(email: str, user_update: UserEdit):
    existing_user = await users_collection.find_one({"email": email})
    if not existing_user:
        raise Exception("User doesn't exists")
    updates = {}

    if user_update.email:
        updates["email"] = user_update.email
    if user_update.password:
        updates["password"] = hash_password(user_update.password)

    if updates:
        await users_collection.update_one({"email": email}, {"$set": updates})
        existing_user.update(updates)  # update local dict with changes

    return existing_user

async def authenticate_user(email: str, password: str):
    user = await users_collection.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        return None
    return create_jwt_token({"email": user["email"]})

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# async def create_user(user_data):
#     existing_user = await users_collection.find_one({"email": user_data.email})
#     if existing_user:
#         return None
#     hashed_password = pwd_context.hash(user_data.password)
#     user = {
#         "username": user_data.username,
#         "email": user_data.email,
#         "password": hashed_password
#     }
#     await users_collection.insert_one(user)
#     return create_jwt_token({"email": user["email"]})
