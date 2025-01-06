from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth import router
from .core.config import settings
from .db.base import Base



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



@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

app.include_router(router, prefix=settings.API_V1_STR)
