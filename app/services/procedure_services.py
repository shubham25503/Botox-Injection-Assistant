from app.schemas.procedure_schema import ProcedureCreate, ProcedureEdit, ProcedureOut
from app.database import procedure_collection, users_collection 
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException

async def create_procedure(procedure_data: dict, current_user):
    current_user = await users_collection.find_one({"email": current_user["email"]})
    procedure_data["doctor_id"] = current_user["_id"]
    
    if isinstance(procedure_data["procedure_date"], datetime):
        pass
    else:
        procedure_data["procedure_date"] = datetime.combine(procedure_data["procedure_date"], datetime.min.time())
    
    result = await procedure_collection.insert_one(procedure_data)
    return str(result.inserted_id)

async def get_all_procedures():
    procedures = []
    async for procedure in procedure_collection.find():
        procedure["_id"] = str(procedure["_id"])
        procedures.append(procedure)
    return procedures

async def get_procedure(procedure_id: str):
    procedure = await procedure_collection.find_one({"_id": ObjectId(procedure_id)})
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    
    procedure['id'] = str(procedure['_id'])  # Optional for frontend
    return ProcedureOut(**procedure)

async def get_all_procedures_for_user(user_id):
    procedures = []
    async for procedure in procedure_collection.find({"doctor_id": ObjectId(user_id)}):
        procedure["_id"] = str(procedure["_id"])
        procedure["doctor_id"] = str(procedure["doctor_id"])
        procedures.append(procedure)
    
    return procedures

async def update_procedure(procedure_id:str,data:ProcedureEdit):
    if not procedure_id:
        raise ValueError("Procedure ID is required.")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if "procedure_date" in update_data:
        update_data["procedure_date"] = datetime.combine(update_data["procedure_date"], datetime.min.time())

    # update_data["updated_at"] = datetime.now()

    result = await procedure_collection.update_one(
        {"_id": ObjectId(procedure_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise ValueError("No procedure found with the given ID.")

    return True

async def delete_procedure(procedure_id:str):
    if not procedure_id:
        raise ValueError("Procedure ID is required.")
    
    result = await procedure_collection.update_one(
        {"_id": ObjectId(procedure_id)},
        {"$set": {"is_deleted": True}}
    )
    if result.matched_count == 0:
        raise ValueError("No procedure found with the given ID.")
    return True

