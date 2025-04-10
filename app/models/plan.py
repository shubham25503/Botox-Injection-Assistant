from pydantic import BaseModel
from typing import Optional
from bson import ObjectId

class PlanBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    duration: str  
    stripe_price_id: Optional[str] = None  

