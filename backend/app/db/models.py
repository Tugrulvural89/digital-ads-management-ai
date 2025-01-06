from sqlalchemy import JSON, Boolean, Column, Text, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import Enum 
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    facebook_access_token = Column(String, nullable=True, index=True)
    google_credentials = Column(JSON, nullable=True)

    ad_accounts = relationship("AdAccount", back_populates="user")

class ChannelType(str, Enum):
    GOOGLE = "google"
    FACEBOOK = "facebook"


class AdAccount(Base):
    __tablename__ = 'ad_accounts'

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(String, unique=True, index=True, nullable=False)
    channel = Column(String, nullable=False , index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # Nullable foreign key
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="ad_accounts")
    ad_campaigns = relationship("AdCampaign", back_populates="ad_account")
    recommendations = relationship("Recommendation", back_populates="ad_account")
    

class AdCampaign(Base):
    __tablename__ = "ad_campaigns"

    id = Column(Integer, primary_key=True, index=True)
    ad_account_id = Column(Integer, ForeignKey("ad_accounts.id"), nullable=True, index=True)  # Nullable foreign key
    name = Column(String, nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ad_account = relationship("AdAccount", back_populates="ad_campaigns")
    ad_creatives = relationship("AdCreative", back_populates="ad_campaign")
    recommendations = relationship("Recommendation", back_populates="ad_campaign")



class AdCreative(Base):
    __tablename__ = "ad_creatives"

    id = Column(Integer, primary_key=True, index=True)
    ad_campaign_id = Column(Integer, ForeignKey("ad_campaigns.id"), nullable=True, index=True)  # Nullable foreign key
    name = Column(String, nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ad_campaign = relationship("AdCampaign", back_populates="ad_creatives")
    recommendations = relationship("Recommendation", back_populates="ad_creative")



class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    ad_account_id = Column(Integer, ForeignKey("ad_accounts.id"), nullable=True, index=True)
    ad_campaign_id = Column(Integer, ForeignKey("ad_campaigns.id"), nullable=True, index=True)
    ad_creative_id = Column(Integer, ForeignKey("ad_creatives.id"), nullable=True, index=True)
    recommendation_text = Column(Text, nullable=False)
    status = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    ad_account = relationship("AdAccount", back_populates="recommendations")
    ad_campaign = relationship("AdCampaign", back_populates="recommendations")
    ad_creative = relationship("AdCreative", back_populates="recommendations")
