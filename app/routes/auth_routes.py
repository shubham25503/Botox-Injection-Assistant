from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserLogin, UserOut, UserSignup, UserEdit, ResetPassword
from app.services.auth_service import create_user, authenticate_user,  update_user, forgot_password
from app.utils.jwt_handler import get_current_user_email
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=UserOut)
async def signup(user: UserSignup):
    try:
        new_user =await create_user(user)
        return new_user
    except Exception as e:
        print("signup",e)
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
async def login(user: UserLogin):
    try:
        token = await authenticate_user(user.email, user.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return {"access_token": token}
    except Exception as e:
        print("login", e)
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = await authenticate_user(form_data.username, form_data.password)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        print("login", e)
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/reset_password")
async def reset_password(data: ResetPassword):
    try:
        await forgot_password(data.email)
        return {"message": "Temporary password sent to your email"}
    except Exception as e:
        print("edit", e)
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/edit", response_model=UserOut)
async def edit_user(data: UserEdit, user_email: str = Depends(get_current_user_email)):
    try:
        print(user_email)
        updated = await update_user(user_email, data)
        return updated
    except Exception as e:
        print("edit", e)
        raise HTTPException(status_code=400, detail=str(e))
    
