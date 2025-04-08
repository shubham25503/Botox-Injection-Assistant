from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class DoseEntry(BaseModel):
    dose_number: int
    pre_image_url: Optional[str] = None
    ai_predicted_image_url: Optional[str] = None
    post_image_url: Optional[str] = None
    follow_up_image_url: Optional[str] = None

class ImageData(BaseModel):
    procedure_id: str
    doctor_id: str
    patient_name: str
    injection_areas: List[str]
    doses: List[DoseEntry]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_deleted: bool = False
