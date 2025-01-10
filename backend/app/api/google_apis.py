from fastapi import APIRouter, Depends, HTTPException
from requests import Session

from ..db.schemas import GoogleGetAuthResponse

from .token import get_current_user
from ..core.config import settings
from ..db.models import AdAccount, User
from ..db.session import get_db
from ..services.google_ads import GoogleAdsService
import requests


router = APIRouter(prefix=settings.API_V1_STR_GOOGLE, tags=["Google Ads"])

@router.post("/fetch-campaigns")
async def fetch_campaigns(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    try:
        # Kullanıcı doğrulama
        user = db.query(User).filter(User.user_email == current_user.user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        google_credentials_dict = user.google_credentials
        if not google_credentials_dict:
            raise HTTPException(status_code=400, detail="Google credentials not found")

        # En son eklenen AdAccount'u al
        latest_ad_account = db.query(AdAccount).filter(AdAccount.user_id == user.id).order_by(AdAccount.created_at.desc()).first()
        if not latest_ad_account:
            raise HTTPException(status_code=404, detail="No ad accounts found for this user")

        customer_id = latest_ad_account.account_id

        # GoogleAdsService oluştur
        google_ads_service = GoogleAdsService(
            credentials={
                "token": google_credentials_dict.get("token"),
                "refresh_token": google_credentials_dict.get("refresh_token"),
                "token_uri": "https://accounts.google.com/o/oauth2/token",
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "scopes": ["https://www.googleapis.com/auth/adwords"]
            },
            developer_token=settings.GOOGLE_DEVELOPER_TOKEN,
            login_customer_id=customer_id
        )

        # Kampanyaları getir
        campaigns = google_ads_service.fetch_campaigns(customer_id=customer_id)
        return {"campaigns": campaigns}

    except HTTPException as http_ex:
        raise http_ex
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching campaigns: {str(e)}")


@router.post("/auth")
async def auth_google(request: GoogleGetAuthResponse, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Handles Google authorization, returns access and refresh tokens.
    """
    try:
        user = db.query(User).filter(User.user_email == current_user.user_email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Send token request to Google
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "code": request.code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
            },
        )
        response.raise_for_status()
        token_data = response.json()

        # Extract access and refresh tokens
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        print(access_token)
        print("refresh_token :", refresh_token)
        return {"access_token": access_token, "refresh_token": refresh_token}

    except requests.exceptions.RequestException as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"Google API request error: {e}")


@router.post("/auth/refresh")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """
    Refresh the access token using the provided refresh token.
    """
    try:
        # Send refresh token request to Google
        response = requests.post(
            "https://oauth2.googleapis.com/token",
            data={
                "refresh_token": refresh_token,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "grant_type": "refresh_token",
            },
        )
        response.raise_for_status()
        token_data = response.json()

        # Get the new access token
        access_token = token_data.get("access_token")

        # ... (Update access token in database) ...

        return {"access_token": access_token}

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Token refresh error: {e}")

