from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserSignup(BaseModel):
    username:str
    email: EmailStr
    password: str
    plan: str  # monthly, semiannual, annual


class UserLogin(BaseModel):
    email: str
    password: str

class UserEdit(BaseModel):
    username:Optional[str]
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    access_expires :  Optional[datetime]

class UserOut(BaseModel):
    email: EmailStr
    access_code: Optional[str]
    access_expires: Optional[datetime]

class ResetPassword(BaseModel):
    email: EmailStr