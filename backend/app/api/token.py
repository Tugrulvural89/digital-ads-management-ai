from fastapi import Depends, Form, HTTPException, Header, status
from fastapi.security import OAuth2AuthorizationCodeBearer
from requests import Session
from ..core.config import settings
from datetime import datetime, timedelta
from typing import List, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
from ..core.config import settings
from ..db.models import User
from ..db.session import get_db

# --- Authentication ---

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token", authorizationUrl="/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(user_email: str, password: str, db: Session):
    user = db.query(User).filter(User.user_email == user_email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "sub": data["sub"]})  # Use username or email
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_email: str = payload.get("sub")  # Extract username or email
        if user_email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.user_email == user_email).first()  # Lookup user by username or email
    if user is None:
        raise credentials_exception
    return user

from jose import JWTError, jwt
from datetime import datetime
from fastapi import HTTPException, status

def verify_access_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Token'ı çözme ve validate etme
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Expiration süresi kontrolü
        if datetime.now() > datetime.now(payload["exp"]):
            raise credentials_exception  # Token süresi dolmuş
        
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception

        return payload
    except JWTError:
        raise credentials_exception
