from pydantic import BaseModel
from typing import List
from bson import ObjectId
from datetime import datetime
from typing import Optional

class ProcedureCreate(BaseModel):
    patient_name: str
    patient_gender: str
    patient_age: int
    institution_name: str
    procedure_date: datetime
    injection_areas: List[str]
    is_deleted: bool = False

class ProcedureEdit(BaseModel):
    patient_name: Optional[str] = None
    patient_gender: Optional[str] = None
    patient_age: Optional[int] = None
    institution_name: Optional[str] = None
    procedure_date: Optional[datetime] = None
    injection_areas: Optional[List[str]] = None
    is_deleted: Optional[bool] = None

class ProcedureOut(BaseModel):
    patient_name: str
    institution_name: str
    procedure_date: datetime
    injection_areas: List[str]
    is_deleted: bool = False

    class Config:
        orm_mode = True
        json_encoders = {
            ObjectId: str
        }