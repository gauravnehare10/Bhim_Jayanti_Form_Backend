from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from config.database import user_collection, SECRET_KEY
from models.models import UserInDB, TokenData
from passlib.context import CryptContext
from datetime import timedelta, datetime
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_DAYS = 1
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: timedelta | None):
    to_encode = data.copy()
    to_encode.update({
        "exp": datetime.utcnow() + expires_delta,
        "scope": "access"
    })
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_user(username: str):
    user_dict = await user_collection.find_one({"username": username})
    if user_dict:
        user_dict["userId"] = user_dict.pop("_id", None)
        return UserInDB(**user_dict)
    return None

def hash_password(password: str):
    pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("scope") != "access":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token scope. Use an access token."
            )
        usename = payload.get("sub")
        if usename is None:
            raise credentials_exception
        
        token_data = TokenData(username=usename)
    except InvalidTokenError:
        raise credentials_exception
    
    user = await get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    
    return user