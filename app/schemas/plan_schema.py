from app.models.plan import PlanBase
from pydantic import BaseModel
from typing import Optional

class PlanCreate(PlanBase):
    pass

class PlanUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    stripe_price_id: Optional[str] = None

class PlanInDB(PlanBase):
    id: str

class PlanOut(BaseModel):
    name: str
    price: float
    description: str
    duration: str
    
