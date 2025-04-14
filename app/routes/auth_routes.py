from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user_schema import UserLogin, UserOut, UserSignup, UserEdit, ResetPassword, UserOut2
from app.services.auth_service import create_user, authenticate_user,  update_user, forgot_password, get_data
# from app.utils.jwt_handler import get_current_user_email
from app.utils.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.functions import create_response, handle_exception

router = APIRouter(tags=["auth"])


@router.post("/signup")
async def signup(user: UserSignup):
    try:
        new_user =await create_user(user)
        return create_response(200,True,"User Created Successfully",new_user)
    except Exception as e:
        print("signup",e)
        raise HTTPException(status_code=400, detail=handle_exception(e, "Error creating user"))

@router.post("/login")
async def login(user: UserLogin):
    try:
        token = await authenticate_user(user.email, user.password)
        if not token:
            raise HTTPException(status_code=401, detail=handle_exception(e, "Invalid email or password", 401))
        return create_response(200,True,"Login Successfully",{"access_token": token})
    
    except Exception as e:
        print("login", e)
        raise HTTPException(status_code=401, detail=handle_exception(e, "Error creating user", 401))


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token = await authenticate_user(form_data.username, form_data.password)
        if not token:
            raise HTTPException(status_code=401, detail=handle_exception(e, "Invalid email or password", 401))
        return create_response(200,True,"token generated successfully",{"access_token": token, "token_type": "bearer"})
    except Exception as e:
        print("token", e)
        raise HTTPException(status_code=401,detail=handle_exception(e,"bad token generation",401))

@router.post("/reset-password")
async def reset_password(data: ResetPassword):
    try:
        await forgot_password(data.email)
        return create_response(200,True, "Temporary password sent to your email",None)
    except Exception as e:
        print("reset-password", e)
        raise HTTPException(status_code=400, detail=handle_exception(e,"email can't be sent"))

# @router.put("/edit", response_model=UserOut)
@router.put("/edit/{user_id}", dependencies=[Depends(get_current_user)])
async def edit_user(data: UserEdit, user_id: str):
    try:
        # print(user_email)
        updated = await update_user(user_id, data)
        return create_response(200,True,"User data Edited Successfully",updated)
    except Exception as e:
        print("edit", e)
        raise HTTPException(status_code=400, detail=handle_exception(e,"User Can't Be Edited"))
    

# @router.get("/user/details", response_model=UserOut2)
@router.get("/user/details/{user_id}", dependencies=[Depends(get_current_user)])
async def get_user_data(user_id:str):
    try:
        data=await get_data(user_id)
        return create_response(200,True,"user data fetched",data)
    except Exception as e:
        print("get-data", e)
        raise HTTPException(status_code=400, detail=handle_exception(e,"Can't Fetch User Detail"))
    