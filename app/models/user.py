from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_admin: bool = False
    payment_status: Optional[bool] = None 
    # access_code: Optional[str] = None
    # access_expires: Optional[datetime] = None
    created_at: datetime = datetime.now()

    class Config:
        from_attributes = True
