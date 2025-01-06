from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from ..core.config import settings

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://example_user:example_password@localhost:55000/example_db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
