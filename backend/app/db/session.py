from .base import SessionLocal

def get_db():
    """
    Dependency function to get the database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        