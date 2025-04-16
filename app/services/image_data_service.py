from app.database import image_data_collection, procedure_collection, users_collection
from datetime import datetime
from bson import ObjectId
from app.utils.functions import convert_objectid_and_datetime
from app.config import STABLE_DIFFUSION
import json
import requests

async def create_image_data(procedure_id: str, user: str, data):
    # print(procedure_id,doctor_data,data)
    doctor_data=await users_collection.find_one({"email":user["email"]})
    doctor_id=doctor_data["_id"]
    # print(doctor_id)
    procedure = await procedure_collection.find_one({"_id": ObjectId(procedure_id)})
    if not procedure:
        raise Exception("Procedure not found.")

    image_data_doc = {
        "procedure_id": ObjectId(procedure_id),
        "doctor_id":  doctor_id,
        "patient_name": procedure["patient_name"],
        "injection_areas": procedure["injection_areas"],
        "doses": [dose.dict() for dose in data.doses],
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "is_deleted": False,
    }

    result = await image_data_collection.insert_one(image_data_doc)
    return str(result.inserted_id)

async def update_image_data(procedure_id: str, data):
    # print(procedure_id)
    new_doses = [dose.dict() for dose in data.doses]

    result = await image_data_collection.update_one(
        {"procedure_id": ObjectId(procedure_id)},
        {
            "$push": {"doses": {"$each": new_doses}},  
            "$set": {"updated_at": datetime.now()}  
        }
    )

    if result.matched_count == 0:
        raise Exception("Image data not found.")

async def get_image_generated(procedure_id: str):
    url=STABLE_DIFFUSION
    responses=[]
    data = await procedure_collection.find_one({"_id": ObjectId(procedure_id), "is_deleted": False})
    if not data["image_path"]:
        raise Exception("Image data not found.")
    file_path=data["image_path"]
    injection_areas_data = json.loads(data["injection_areas"])
    print(injection_areas_data)
    for area in injection_areas_data:
        if area["selected"]==True:
            payload={
                'injection_number': area["units"],  # Ensure this is a string representation of an integer
                'selected_area': area["name"]  
            }
            print(payload)
            files = {
                'file': open(file_path, 'rb')
            }

            response = requests.post(url, data=payload, files=files)
            try:
                result_data = response.json()
            except Exception:
                result_data = {"raw_response": response.text}

            result_data["units"] = area["units"]
            result_data["selected_area"] = area["name"]


            responses.append(result_data)
    # data["_id"] = str(data["_id"])
    # return convert_objectid_and_datetime(data)
    return responses