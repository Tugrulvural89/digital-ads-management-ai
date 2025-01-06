from fastapi import APIRouter, Body, Depends, Form, HTTPException, Header, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from requests import Session
import requests
from google.auth.transport.requests import Request
from ..services.google_ads import GoogleAdsService


from ..core.config import settings

from datetime import datetime, timedelta
from typing import List, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from ..core.config import settings
from ..db.models import AdAccount, User
from ..db.session import get_db
from ..db.schemas import AdAccountCreate, GoogleCredentials, GoogleSignInRequest, Token, UserCreate, UserData

import os
import google.oauth2.id_token
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.oauth2 import id_token
from google.auth.exceptions import GoogleAuthError

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import google.ads.googleads.client
router = APIRouter()


# --- Authentication ---

oauth2_scheme = OAuth2AuthorizationCodeBearer(tokenUrl="token", authorizationUrl="localhost:8010")
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

# --- API Routes ---

class TokenRequest(BaseModel):
    user_email: str
    password: str

@router.post("/token", response_model=Token)
async def login_for_access_token(
    request: TokenRequest,  # Accept JSON payload
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    # Authentication logic
    user = authenticate_user(request.user_email, request.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Generate token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": request.user_email}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}



async def get_current_user_id(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception
    


# User

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/users/", response_model=UserData)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """

    existing_user = db.query(User).filter(User.user_email == user.user_email).first()
    if existing_user:
        raise ValueError("User with this email already exists.")


    # Hash the password
    hashed_password = pwd_context.hash(user.password)

    # Create a new user instance
    db_user = User(
        user_email=user.user_email,
        hashed_password=hashed_password,
        created_at=datetime.now(),  # Use UTC time
        updated_at=datetime.now()   # Use UTC time
    )

    
    try:
        db.add(db_user)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        return db_user


# Endpoint to list all users
@router.get("/getusers/")
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


# enduser

@router.post("/update-google-credentials")
def update_google_credentials(credentials: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.google_credentials = credentials
    db.commit()
    return {"message": "Google credentials updated successfully"}



@router.post("/google/callback")
async def callback_google(request: GoogleSignInRequest, db=Depends(get_db)):
    try:
        # Verify the Google credential
        id_info = id_token.verify_oauth2_token(
            request.credential,
            requests.Request(),
            settings.GOOGLE_CLIENT_ID
        )

        # Find the user in the database
        user = db.query(User).filter(User.user_email == id_info['email']).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        # Store Google credentials in the User model
        user.google_credentials = {
            'token': id_info.get('sub'),  # Google user ID
            'access_token': id_info.get('access_token'),  # Access token
            'refresh_token': id_info.get('refresh_token'),  # Refresh token (if available)
            'token_uri': 'https://oauth2.googleapis.com/token',
            'client_id': settings.GOOGLE_CLIENT_ID,
            'client_secret': settings.GOOGLE_CLIENT_SECRET,
            'scopes': ['https://www.googleapis.com/auth/adwords']
        }
        db.commit()

        # Fetch Google Ads account IDs
        google_ads_service = GoogleAdsService(
            credentials=user.google_credentials,
            developer_token=settings.GOOGLE_DEVELOPER_TOKEN
        )
        
        # Get the list of accessible Google Ads accounts
        ad_accounts = google_ads_service.get_ad_accounts()

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Google credentials saved successfully", "ad_accounts": ad_accounts}
        )
    except GoogleAuthError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google authentication failed")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



class SaveCredentialsRequest(BaseModel):
    credentials: GoogleCredentials
    user_email: str

@router.post("/save-credentials")
async def save_google_credentials(
    request: SaveCredentialsRequest, 
    db: Session = Depends(get_db)
):
    try:
        # Fetch the user by email
        user = db.query(User).filter(User.user_email == request.user_email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update user's Google credentials
        user.google_credentials = {
            "access_token": request.credentials.access_token,
            "scope": request.credentials.scope,
            "refresh_token": request.credentials.refresh_token,
            "expires_in": request.credentials.expires_in,
            "token_type": request.credentials.token_type
        }

        # Commit changes to the database
        db.add(user)
        db.commit()
        db.refresh(user)

        return JSONResponse(content={"message": "Credentials saved successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving credentials: {str(e)}")


class AccessTokenRequest(BaseModel):
    access_token: str

@router.post("/google-ad-accounts")
async def get_google_ad_accounts(request: AccessTokenRequest):
    try:
        

        developer_key = settings.GOOGLE_DEVELOPER_TOKEN
        access_token = request.access_token
        
         # Endpoint URL
        url = f"https://googleads.googleapis.com/v17/customers:listAccessibleCustomers?access_token={access_token}"

         
        # Headers
        # Set up headers
        headers = {
            "Authorization": f"Bearer {access_token}",
            "developer-token": developer_key,
            "Accept": "application/json"
        }

        # Make the GET request using the requests library
        response = requests.get(url, headers=headers)

        # Check for HTTP errors
        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code, 
                detail=f"Failed to fetch Google Ads accounts: {response.text}"
            )

        # Return the response JSON
        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching accounts: {str(e)}")


class SaveAdAccountRequest(BaseModel):
    account_id: str
    user_email: str
    channel: str

@router.post("/save-ad-account")
async def save_ad_account(
    request: SaveAdAccountRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Check if the AdAccount already exists for the user
        existing_account = db.query(AdAccount).filter(
            AdAccount.account_id == request.account_id,
            AdAccount.user_email == current_user.user_email
        ).first()

        if existing_account:
            # If the account exists, update it
            existing_account.account_id = request.account_id
            existing_account.channel = request.channel  # Assuming you need to update channel too
            db.commit()
            db.refresh(existing_account)
            return {"message": "Ad account updated successfully", "ad_account": existing_account}
        
        # If the account does not exist, create a new one
        ad_account = AdAccount(
            account_id=request.account_id,
            channel=request.channel,
            user_id=current_user.id  # Link to the current user
        )
        db.add(ad_account)
        db.commit()
        db.refresh(ad_account)

        # Optionally, update the user's google_credentials with the selected account
        current_user.google_credentials.update({
            "selected_account_id": ad_account.account_id,
            "selected_account_name": request.account_id  # You could update the name as well if available
        })
        db.commit()

        return {"message": "Ad account saved successfully", "ad_account": ad_account}
    
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=500, detail=str(e))
