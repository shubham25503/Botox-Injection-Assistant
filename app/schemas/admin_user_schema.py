from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class AdminUserBase(BaseModel):
    username: str
    email: EmailStr
    is_admin: bool = False

class AdminUserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr]=None
    is_admin: Optional[bool]=None
    password : Optional[str] = None

class AdminUserResponse(AdminUserBase):
    id: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True
