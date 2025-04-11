from pydantic import BaseModel, Field
from typing import List
from datetime import date
from bson import ObjectId
from datetime import datetime

class Procedure(BaseModel):
    patient_name: str
    institution_name: str
    doctor_id: str
    procedure_date: date
    injection_areas: List[str]
    is_deleted:bool 
    created_at: datetime = datetime.now()


    class Config:
        arbitrary_types_allowed = True
