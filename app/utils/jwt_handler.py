import jwt
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM

def create_jwt_token(data: dict):
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    payload.update({"exp": expire})
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token  
