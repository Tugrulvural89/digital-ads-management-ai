from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME : str = "Ads Dashboard"
    API_V1_STR: str = "/api/v1"
    API_V1_STR_GOOGLE: str = "/api/v1/google"
    DB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:8010", 
        "http://localhost:8000", 
        "http://127.0.0.1:8010", 
        "http://127.0.0.1:8000", 
        "https://accounts.google.com",
        "https://oauth2.googleapis.com",
        # ... other origins
    ]

    
    # GOOGLE ADS API CREDENTIALS
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    #GOOGLE_REFRESH_TOKEN: str
    GOOGLE_DEVELOPER_TOKEN: str
    GOOGLE_MANAGER_ID: str  
    GOOGLE_REDIRECT_URI: str  

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
