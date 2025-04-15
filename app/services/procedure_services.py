from app.schemas.procedure_schema import ProcedureCreate, ProcedureEdit, ProcedureOut
from app.database import procedure_collection, users_collection 
from datetime import datetime
from bson import ObjectId
from fastapi import HTTPException
from app.utils.functions import objectid_to_str
from fastapi.encoders import jsonable_encoder
import os

async def create_procedure(procedure_data: dict, current_user):
    current_user = await users_collection.find_one({"email": current_user["email"]})
    procedure_data["doctor_id"] = current_user["_id"]
    if "," in procedure_data["injection_areas"][0] and len(procedure_data["injection_areas"])!=8:
        procedure_data["temp_list"]=procedure_data["injection_areas"][0].split(",")
        if len(procedure_data["temp_list"])== 8:
            procedure_data["injection_areas"]=procedure_data["temp_list"]
            del procedure_data["temp_list"]
    
    else:
        raise HTTPException(status_code=500)
    
    if isinstance(procedure_data["procedure_date"], datetime):
        pass
    else:
        procedure_data["procedure_date"] = datetime.combine(procedure_data["procedure_date"], datetime.min.time())
    
    result = await procedure_collection.insert_one(procedure_data)
    data =await procedure_collection.find_one({"_id":result.inserted_id})
    data["_id"]=str(data["_id"])
    data["doctor_id"]=str(data["doctor_id"])
    return data

async def get_all_procedures():
    procedures = []
    async for procedure in procedure_collection.find():
        if not procedure["is_deleted"]:
            del procedure["is_deleted"]
            procedures.append(procedure)
    # Use jsonable_encoder to handle serialization of ObjectId and other special cases
    return jsonable_encoder(procedures, custom_encoder={ObjectId: objectid_to_str})

async def get_procedure(procedure_id: str):
    procedure = await procedure_collection.find_one({"_id": ObjectId(procedure_id)})
    if not procedure:
        raise HTTPException(status_code=404, detail="Procedure not found")
    
    procedure['_id'] = str(procedure['_id'])  # Optional for frontend
    procedure['doctor_id'] = str(procedure['doctor_id'])  # Optional for frontend
    return {**procedure}

async def get_all_procedures_for_user(user_id):
    procedures = []
    async for procedure in procedure_collection.find({"doctor_id": ObjectId(user_id)}):
        procedure["_id"] = str(procedure["_id"])
        procedure["doctor_id"] = str(procedure["doctor_id"])
        if not procedure["is_deleted"]:
            del procedure["is_deleted"]
            procedures.append(procedure)
    
    return procedures

async def edit_image_procedure(procedure_id:str,image):
    try:
        procedure = await procedure_collection.find_one({"_id": ObjectId(procedure_id)})

        if not procedure:
            raise HTTPException(status_code=404, detail="Procedure not found")

        current_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(os.path.dirname(current_dir))
        new_current_dir = os.getcwd()
        patient_dir = os.path.join(new_current_dir, f"uploads/{procedure['patient_name']}")
        os.makedirs(patient_dir, exist_ok=True)

        image_path = os.path.join(patient_dir, f"dose_0.jpg")
        with open(image_path, "wb") as f:
            f.write(await image.read())

        await procedure_collection.update_one(
            {"_id": ObjectId(procedure_id)},
            {"$set": {"image_path": image_path}}
        )

        updated_procedure = await procedure_collection.find_one({"_id": ObjectId(procedure_id)})
        updated_procedure["_id"] = str(updated_procedure["_id"])
        updated_procedure["doctor_id"] = str(updated_procedure["doctor_id"])

        return updated_procedure

    except Exception as e:
        raise HTTPException(status_code=500)

    
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

