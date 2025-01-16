from enum import Enum
from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt
from models import User
from passlib.context import CryptContext

# JWT Configuration
SECRET_KEY = "877a59a92dfc5aac378061e6c5fdd1a677881514fb28677a621d613c05883a05"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _hash_pwd(original_pwd: str) -> str:
    return _pwd_context.hash(original_pwd)

def _verify_pwd(checked_pwd: str, hashed_pwd: str)-> bool:
    return _pwd_context.verify(checked_pwd, hashed_pwd)

def _db_user_not_valid(db_user, pwd: str)-> bool:
    return db_user is None or not _verify_pwd(pwd, db_user.hashed_pwd)

def _fetch_db_user(db, username, pwd)-> User:
    db_user = db.query(User).filter(User.username == username).first()
    if _db_user_not_valid(db_user, pwd):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user

def _create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def fetch_user(uid: str, db: Session) -> dict:
    user = db.query(User).filter(User.uid == uid).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with uid '{uid}' not found")
    return user

def login(username: str, pwd: str, db: Session) -> dict[str, str]:
    db_user = _fetch_db_user(db, username, pwd)
    access_token = _create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

def register_user(
        username: str, 
        pwd: str, 
        email: str,
        phone_num: str,
        age: int,
        gender: Enum,
        db: Session,
    ) -> dict:
    """
    Will try to register a user using a username, pwd and a database.
    Fails if the username, email or phone number is taken.
    """
    same_name_user = db.query(User).filter(User.username == username).first()
    if same_name_user != None:
        raise HTTPException(status_code=400, detail="Username already exists")
    same_email_user = db.query(User).filter(User.email == email).first()
    if same_email_user != None:
        raise HTTPException(status_code=400, detail="Email already exists")
    same_phone_user = db.query(User).filter(User.phone_num == phone_num).first()
    if same_phone_user != None:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    hashed_pwd = _hash_pwd(pwd)
    new_user = User(
        username=username, 
        hashed_pwd=hashed_pwd,
        email=email,
        phone_num=phone_num,
        age=age,
        gender=gender
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user.to_dict()


def update_user(
        uid: str,
        username: str|None, 
        pwd: str|None, 
        email: str|None,
        phone_num: str|None,
        age: int|None,
        gender: Enum|None,
        db: Session,
    ):
    """
    Will try to update a user using a uid.
    Fails if the username, email or phone number is taken.
    Also fails if the uid can't be found in the database.
    """
    same_name_user = db.query(User).filter(User.username == username).first()
    if same_name_user != None:
        raise HTTPException(status_code=400, detail="Username already exists")
    same_email_user = db.query(User).filter(User.email == email).first()
    if same_email_user != None:
        raise HTTPException(status_code=400, detail="Email already exists")
    same_phone_user = db.query(User).filter(User.phone_num == phone_num).first()
    if same_phone_user != None:
        raise HTTPException(status_code=400, detail="Phone number already exists")

    user = db.query(User).filter(User.uid == uid).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with uid '{uid}' not found")
    if username!=None:
        user.username = username
    if pwd!=None:
        user.hashed_pwd= _hash_pwd(pwd)
    if email!=None:
        user.email = email
    if phone_num!=None:
        user.phone_num = phone_num
    if age!=None:
        user.age = age
    if gender!=None:
        user.gender = gender
    db.commit()

def delete_user(uid: str, db: Session):
    user_to_delete = db.query(User).filter(User.uid == uid).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail=f"User with uid '{uid}' not found")
    db.delete(user_to_delete)
    db.commit()
