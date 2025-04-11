from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["botox"]
users_collection = db["users"]
procedure_collection = db["procedures"]
plan_collection = db["plans"]
image_data_collection = db["image_data"]
