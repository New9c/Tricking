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

def _verify_age(age: int|None)-> bool:
    if age==None:
        return True
    if 0<=age<=200:
        return True
    return False

def _verify_username(username: str|None)-> bool:
    if username==None:
        return True
    for c in username:
        if c=='@':
            return False
    return True

def _verify_email(email: str|None)-> bool:
    if email==None:
        return True
    for c in email:
        if c=='@':
            return True
    return False

def _verify_phone(phone: str|None)-> bool:
    if phone==None:
        return True
    for c in phone:
        if ord(c)>ord('9') or ord(c)<ord('0'):
            return False
    return True

def _check_for_same_user(username, email, phone_num, db):
    same_name_user = db.query(User).filter(User.username == username).first()
    if same_name_user != None:
        raise HTTPException(status_code=400, detail="Username already exists")
    same_email_user = db.query(User).filter(User.email == email).first()
    if same_email_user != None:
        raise HTTPException(status_code=400, detail="Email already exists")
    same_phone_user = db.query(User).filter(User.phone_num == phone_num).first()
    if same_phone_user != None:
        raise HTTPException(status_code=400, detail="Phone number already exists")

def _verify_params(
        username: str|None, 
        email: str|None,
        phone_num: str|None,
        age: int|None,
        db: Session,
    ):
    if not _verify_username(username) or not _verify_age(age) or not _verify_email(email) or not _verify_phone(phone_num):
        raise HTTPException(status_code=401, detail="Invalid Parameters")
    _check_for_same_user(username, email, phone_num, db)


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

def _fetch_login_user(db, account, pwd)-> User:
    db_user = db.query(User).filter(User.username == account).first()
    if db_user==None:
        db_user = db.query(User).filter(User.email== account).first()
    if db_user==None:
        db_user = db.query(User).filter(User.phone_num== account).first()

    if db_user==None or not _verify_pwd(pwd, db_user.hashed_pwd):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return db_user

def login(account: str, pwd: str, db: Session):
    login_user = _fetch_login_user(db, account, pwd)
    access_token = _create_access_token(data={"sub": login_user.username})
    normal_ret = {"access_token": access_token, "token_type": "bearer"}
    return login_user.uid

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
    _verify_params(username, email, phone_num, age, db)

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
    _verify_params(username, email, phone_num, age, db)

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
