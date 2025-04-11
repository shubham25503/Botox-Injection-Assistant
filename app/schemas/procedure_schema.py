from pydantic import BaseModel
from typing import List
from datetime import date
from typing import Optional

class ProcedureCreate(BaseModel):
    patient_name: str
    institution_name: str
    procedure_date: date
    injection_areas: List[str]
    is_deleted:bool= False

class ProcedureEdit(BaseModel):
    patient_name: Optional[str] = None
    institution_name: Optional[str]= None
    procedure_date: Optional[date]= None
    injection_areas: Optional[List[str]]=[]
