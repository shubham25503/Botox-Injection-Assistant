from passlib.context import CryptContext
from app.models.user import users_collection
from app.utils.jwt_handler import create_jwt_token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def create_user(user_data):
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        return None
    hashed_password = pwd_context.hash(user_data.password)
    user = {
        "username": user_data.username,
        "email": user_data.email,
        "password": hashed_password
    }
    await users_collection.insert_one(user)
    return create_jwt_token({"email": user["email"]})

async def authenticate_user(email: str, password: str):
    user = await users_collection.find_one({"email": email})
    if not user or not pwd_context.verify(password, user["password"]):
        return None
    return create_jwt_token({"email": user["email"]})
