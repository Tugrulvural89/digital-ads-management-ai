from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router
from .core.config import settings
from .db.base import Base
from .api.auth import router as auth_router
from .api.google_apis import router as google_router


app = FastAPI()



# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,  # Allow credentials (cookies, authorization headers)
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )


# Auth işlemleri için router ekle
app.include_router(auth_router)

# Google işlemleri için router ekle
app.include_router(google_router)
