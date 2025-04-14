import jwt
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM


security = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def create_jwt_token(data: dict):
    payload = data.copy()
    expire = datetime.now() + timedelta(days=7)
    payload.update({"exp": expire})
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token  

# def get_current_user_email(token: str = Depends(oauth2_scheme)) -> str:
#     try:
#         payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#         print(payload)
#         # print(payload.get("sub"))
#         return payload.get("email")
#     except JWTError:
#         raise HTTPException(status_code=403, detail="Invalid token")
    

def verify_token(token: str):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")