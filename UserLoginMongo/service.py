from enum import Enum
from pymongo.collection import Collection
from fastapi import HTTPException
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from schemas import Gender, User, UserCreate, UserUpdate, UserLogin

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

def _verify_params(user: UserCreate|UserUpdate, collection: Collection):
    if not _verify_username(user.username) or not _verify_age(user.age) or not _verify_email(user.email) or not _verify_phone(user.phone):
        raise HTTPException(status_code=401, detail="Invalid Parameters")


def _create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    access_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return access_token

def fetch_user(check_username, check_email, check_phone, collection: Collection):
    user = collection.find_one({"username": check_username})
    if user==None:
        user = collection.find_one({"email": check_email})
    if user==None:
        user = collection.find_one({"phone": check_phone})
    return user

def login(user: UserLogin, collection: Collection):
    # check username, email and phone with account
    login_user = fetch_user(user.account, user.account, user.account, collection)

    if login_user==None:
        raise HTTPException(status_code=404, detail="No User Found")
    if not _verify_pwd(user.password, login_user["password"]):
        raise HTTPException(status_code=401, detail="Password Invalid")
    access_token = _create_access_token(data={"sub": login_user["username"]})
    normal_ret = {"access_token": access_token, "token_type": "bearer"}

def register_user(user: UserCreate, collection: Collection):
    """
    Will try to register a user using a UserCreate class and a database.
    Fails if the username, email or phone number is taken.
    """
    if fetch_user(user.username, user.email, user.phone, collection)!=None:
        raise HTTPException(status_code=400, detail="User Already Exists")
    _verify_params(user, collection)

    user.password = _hash_pwd(user.password)
    collection.insert_one(user.model_dump())

"""
def update_user(user: UserUpdate, collection: Collection):
    "
    Will try to update a user using a uid.
    Fails if the username, email or phone number is taken.
    Also fails if the uid can't be found in the database.
    "
    _verify_params(user, collection)

    user = db.query(User).filter(User.uid == uid).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with uid '{uid}' not found")
    if username!=None:
        user.username = username
    if pwd!=None:
        user.hashed_pwd= _hash_pwd(pwd)
    if email!=None:
        user.email = email
    if phone!=None:
        user.phone = phone
    if age!=None:
        user.age = age
    if gender!=None:
        user.gender = gender

def delete_user(account: str, collection: Collection):
    user_to_delete = db.query(User).filter(User.uid == uid).first()
    if user_to_delete is None:
        raise HTTPException(status_code=404, detail=f"User with uid '{uid}' not found")
    db.delete(user_to_delete)
    db.commit()
"""
