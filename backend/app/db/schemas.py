from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class GoogleCredentials(BaseModel):
    access_token: str
    scope: str
    refresh_token: Optional[str] = None  # Optional field for refresh token
    expires_in: Optional[int] = None  # Optional field for token expiry in seconds
    token_type: Optional[str] = None  # Optional field for token type (e.g., 'Bearer')

    

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_email: Optional[str] = None
    
class UserBase(BaseModel):
    user_email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=100)

class UserData(UserBase):
    id: int


    class Config:
        from_attributes = True

class AdAccountBase(BaseModel):
    account_id: str
    channel: str  # "google" or "facebook"

class AdAccountCreate(AdAccountBase):
    pass

class AdAccount(AdAccountBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class AdCampaignBase(BaseModel):
    name: str

class AdCampaignCreate(AdCampaignBase):
    pass

class AdCampaign(AdCampaignBase):
    id: int
    ad_account_id: int
    status: bool

    class Config:
        from_attributes = True

class AdCreativeBase(BaseModel):
    name: str

class AdCreativeCreate(AdCreativeBase):
    pass

class AdCreative(AdCreativeBase):
    id: int
    ad_campaign_id: int
    status: bool

    class Config:
        from_attributes = True

class RecommendationBase(BaseModel):
    recommendation_text: str

class RecommendationCreate(RecommendationBase):
    ad_account_id: int
    ad_creative_id: int | None = None
    ad_campaign_id: int | None = None

class Recommendation(RecommendationBase):
    id: int
    ad_account_id: int
    ad_creative_id: int | None = None
    ad_campaign_id: int | None = None
    status: bool

    class Config:
        from_attributes = True


class GoogleAdsCampaignData(BaseModel):
    campaign_id: int
    campaign_name: str
    impressions: int
    clicks: int
    cost_micros: int


class GoogleLoginResponse(BaseModel):
    success: bool
    message: str
    google_ads_account_id: Optional[str] = None


class GoogleSignInRequest(BaseModel):
    credential: str  # Google credential response
