from fastapi import APIRouter, Body, Depends, Form, HTTPException, Header, Request, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2AuthorizationCodeBearer
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel
from requests import Session
import requests
from google.auth.transport.requests import Request

from .token import authenticate_user, create_access_token, get_current_user, get_password_hash, verify_access_token
from ..services.google_ads import GoogleAdsService

from ..core.config import settings

from datetime import datetime, timedelta
from typing import List, Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from ..core.config import settings
from ..db.models import AdAccount, User
from ..db.session import get_db
from ..db.schemas import AccessTokenRequest, AdAccountCreate, GoogleCredentials, GoogleGetAuthResponse, GoogleSignInRequest, SaveAdAccountRequest, Token, TokenRequest, UserCreate, UserData

router = APIRouter(prefix=settings.API_V1_STR, tags=["Auth"])

# --- API Routes ---
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


@router.post("/users/", response_model=UserData)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.user_email == user.user_email).first()
    if existing_user:
        raise ValueError("User with this email already exists.")

    # Hash the password
    hashed_password = get_password_hash(user.password)

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


@router.post("/update-google-credentials")
def update_google_credentials(credentials: dict, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Update Google credentials for the current user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.google_credentials = credentials
    db.commit()
    return {"message": "Google credentials updated successfully"}


@router.post("/save-credentials")
async def save_google_credentials(
    request: GoogleCredentials, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Fetch the user by email
        user = db.query(User).filter(User.user_email == current_user.user_email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update user's Google credentials
        user.google_credentials = {
            "access_token": request.access_token,
            "refresh_token": request.refresh_token,
        }

        # Commit changes to the database
        db.add(user)
        db.commit()
        db.refresh(user)

        return JSONResponse(content={"message": "Credentials saved successfully"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving credentials: {str(e)}")


@router.post("/google-ad-accounts")
async def get_google_ad_accounts(request: AccessTokenRequest):
    try:
        # Fetch Google Ads accounts for the provided access token
        developer_key = settings.GOOGLE_DEVELOPER_TOKEN
        access_token = request.access_token
        
        # Endpoint URL
        url = f"https://googleads.googleapis.com/v17/customers:listAccessibleCustomers?access_token={access_token}"

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
        print(response.json())

        # Return the response JSON
        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching accounts: {str(e)}")


@router.post("/save-ad-account")
async def save_ad_account(
    request: SaveAdAccountRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        # Check if the AdAccount already exists for the user
        existing_account = db.query(AdAccount).filter(
            AdAccount.account_id == str(request.account_id),
            AdAccount.user_id == current_user.id
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

        return {"message": "Ad account saved successfully", "ad_account": ad_account}
    
    except Exception as e:
        print(e)
        db.rollback()  # Rollback in case of an error
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/refresh_token")
def refresh_access_token(refresh_token: str):
    # Refresh token geçerli mi?
    user_data = verify_access_token(refresh_token)
    
    if user_data:
        # Yeni access token oluştur
        new_access_token = create_access_token(data={"sub": user_data["sub"]})
        return {"access_token": new_access_token, "token_type": "bearer"}
    
    # Refresh token geçersiz, login sayfasına yönlendirmek için 401 döndürüyoruz
    raise HTTPException(status_code=401, detail="Invalid refresh token")


