from sqlalchemy.orm import Session
from sqlalchemy import create_engine

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(DATABASE_URL, echo=True)

def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()
