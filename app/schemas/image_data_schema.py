from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class DoseCreate(BaseModel):
    dose_number: int
    pre_image_url: Optional[str]
    ai_predicted_image_url: Optional[str] = None
    post_image_url: Optional[str] = None
    follow_up_image_url: Optional[str] = None

class ImageDataCreate(BaseModel):
    doses: List[DoseCreate]  

class DoseUpdate(BaseModel):
    dose_number: int
    ai_predicted_image_url: Optional[str]
    post_image_url: Optional[str]
    follow_up_image_url: Optional[str]

class ImageDataUpdate(BaseModel):
    doses: List[DoseUpdate]

class ImageDataOut(BaseModel):
    procedure_id: str
    doctor_id: str
    patient_name: str
    injection_areas: List[str]
    doses: List[DoseCreate]
    created_at: datetime
    updated_at: datetime
