from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserSignup(BaseModel):
    username:str
    email: EmailStr
    password: str
    # plan: str = "monthly" # monthly, semiannual, annual


class UserLogin(BaseModel):
    email: str
    password: str

class UserEdit(BaseModel):
    username:Optional[str]
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    # access_expires :  Optional[datetime]

class UserOut(BaseModel):
    email: EmailStr
    access_token: str
    # access_code: Optional[str]
    # access_expires: Optional[datetime]

class ResetPassword(BaseModel):
    email: EmailStr

class UserOut2(BaseModel):
    id:str
    username: str
    email: EmailStr
    # password: str
    is_admin: bool 
    # access_code: Optional[str] = None
    # access_expires: Optional[datetime] = None

class UserBase(BaseModel):
    email : EmailStr
    is_admin : bool