from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin
from app.services.auth_service import create_user, authenticate_user

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate):
    token = await create_user(user)
    if not token:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"access_token": token}

@router.post("/login")
async def login(user: UserLogin):
    token = await authenticate_user(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token}
