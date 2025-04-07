from app.schemas.procedure_schema import ProcedureCreate, ProcedureEdit
from app.database import db
from datetime import datetime
from bson import ObjectId

procedure_collection = db["procedures"]

async def create_procedure(procedure_data: ProcedureCreate):
    procedure_dict = procedure_data.dict()
    if isinstance(procedure_dict["procedure_date"], datetime):
        pass
    else:
        procedure_dict["procedure_date"] = datetime.combine(procedure_dict["procedure_date"], datetime.min.time())
    result = await procedure_collection.insert_one(procedure_dict)
    return str(result.inserted_id)

async def get_all_procedures():
    procedures = []
    async for procedure in procedure_collection.find():
        procedure["_id"] = str(procedure["_id"])
        procedures.append(procedure)
    return procedures

async def update_procedure(procedure_id:str,data:ProcedureEdit):
    if not procedure_id:
        raise ValueError("Procedure ID is required.")

    update_data = {k: v for k, v in data.dict().items() if v is not None}

    if "procedure_date" in update_data:
        # Ensure it's datetime object
        update_data["procedure_date"] = datetime.combine(update_data["procedure_date"], datetime.min.time())

    # update_data["updated_at"] = datetime.utcnow()

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

