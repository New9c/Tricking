from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from models import User
from passlib.context import CryptContext

# JWT Configuration
SECRET_KEY = "877a59a92dfc5aac378061e6c5fdd1a677881514fb28677a621d613c05883a05"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _hash_pwd(original_pwd: str) -> str:
    return _pwd_context.hash(original_pwd)
def _verify_pwd(checked_pwd: str, hashed_pwd: str):
    return _pwd_context.verify(checked_pwd, hashed_pwd)

def _db_user_not_valid(db_user, pwd: str):
    return db_user is None or not _verify_pwd(pwd, db_user.hashed_pwd)

def _fetch_db_user(db, username, pwd)-> User:
    db_user = db.query(User).filter(User.username == username).first()
    if _db_user_not_valid(db_user, pwd):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user

def _create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token


def login(username: str, pwd: str, db: Session):
    db_user = _fetch_db_user(db, username, pwd)
    access_token = _create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def register_user(username: str, pwd: str, db: Session) -> User:
    """
    Will try to register a user using a username, pwd and a database.
    Fails if the username is taken.
    """
    same_name_user = db.query(User).filter(User.username == username).first()
    if same_name_user != None:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_pwd = _hash_pwd(pwd)
    new_user = User(username=username, hashed_pwd=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
