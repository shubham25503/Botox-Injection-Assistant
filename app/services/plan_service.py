from app.database import db
from app.schemas.plan_schema import PlanCreate, PlanUpdate
from bson import ObjectId

collection = db["plans"]

async def create_plan(plan: PlanCreate):
    result = await collection.insert_one(plan.dict())
    created_plan = await collection.find_one({"_id": result.inserted_id})
    return created_plan

async def get_all_plans():
    plans = await collection.find().to_list(100)
    for p in plans:
        p["id"] = str(p["_id"])
        del p["_id"]
    return plans

async def update_plan(plan_id: str, plan: PlanUpdate):
    await collection.update_one(
        {"_id": ObjectId(plan_id)}, {"$set": {k: v for k, v in plan.dict().items() if v is not None}}
    )
    return True

async def delete_plan(plan_id: str):
    await collection.delete_one({"_id": ObjectId(plan_id)})
    return True
