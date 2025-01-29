from pymongo.collection import Collection
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from collections import defaultdict

from user.schemas import UserCreate, UserRoleUpdate, UserUpdate, UserLogin, Role
from config import config

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
        if c=='@' or c==' ':
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

def _verify_params(user: UserCreate|UserUpdate):
    if not _verify_username(user.username) or not _verify_age(user.age) or not _verify_email(user.email) or not _verify_phone(user.phone):
        raise HTTPException(status_code=401, detail="Invalid Parameters")


def _create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    access_token = jwt.encode(to_encode, key=config.SECRET_JWT, algorithm=config.ALGORITHM)
    return access_token

def _fetch_user(check_username, check_email, check_phone, collection: Collection):
    user = collection.find_one({"username": check_username})
    if user==None:
        user = collection.find_one({"email": check_email})
    if user==None:
        user = collection.find_one({"phone": check_phone})
    return user

def fetch_user(username, collection: Collection):
    user = collection.find_one({"username": username})
    if user==None:
        raise HTTPException(status_code=404, detail="User Not Found")
    user.pop("_id")
    return user

def login(form_data: OAuth2PasswordRequestForm, collection: Collection):
    # check username, email and phone with account
    user = UserLogin(account=form_data.username, password=form_data.password)
    login_user = _fetch_user(user.account, user.account, user.account, collection)

    if login_user==None:
        raise HTTPException(status_code=404, detail="User Not Found")
    if not _verify_pwd(user.password, login_user["password"]):
        raise HTTPException(status_code=401, detail="Password Invalid")
    access_token = _create_access_token(data={"sub": login_user["username"]})
    return {"role": login_user["role"], "access_token": access_token, "token_type": "bearer"}

def register_user(user: UserCreate, collection: Collection):
    """
    Will try to register a user using a UserCreate class and a database.
    Fails if the username, email or phone number is taken.
    """
    if _fetch_user(user.username, user.email, user.phone, collection)!=None:
        raise HTTPException(status_code=400, detail="User Already Exists")
    _verify_params(user)

    user.password = _hash_pwd(user.password)
    if collection.count_documents({"role": Role.ADMIN})==0:
        user.role = Role.ADMIN
    collection.insert_one(user.model_dump())

def update_user(username:str, user: UserUpdate, collection: Collection):
    """
    Will try to update a user using a username.
    """
    _verify_params(user)

    update_data = {key: value for key, value in user.model_dump().items() if value!=None}
    if "password" in update_data:
        update_data["password"] = _hash_pwd(update_data["password"])
    if update_data:
        user_to_update  = collection.update_one({"username": username}, {"$set": update_data})
        if user_to_update.modified_count == 0:
            raise HTTPException(status_code=404, detail="User Not Found")
        else:
            return {"status_code": 200}
    else:
        return {"status_code": 200, "msg": "No Data Updated"}

def delete_user(account: str, collection: Collection):
    user_to_delete= _fetch_user(account, account, account, collection)

    if user_to_delete==None:
        raise HTTPException(status_code=404, detail="User Not Found")
    collection.delete_one({"username": user_to_delete["username"]})


def admin_fetch_users(account: str, collection: Collection):
    admin =  _fetch_user(account, account, account, collection)
    if admin==None:
        raise HTTPException(status_code=404, detail="Admin Not Found")
    elif admin["role"]!="admin":
        raise HTTPException(status_code=403, detail="Not Admin")
    users = collection.find({ "role": { "$ne": "admin" } })
    group = defaultdict(set)
    for user in users:
        group[user["role"]].add(user["username"])
    group_json = {}
    if "teacher" in group:
        group_json["teacher"] = group["teacher"]
    if "student_advanced" in group:
        group_json["student_advanced"] = group["student_advanced"]
    if "student_beginner" in group:
        group_json["student_beginner"] = group["student_beginner"]
    return group_json


def admin_update_user_role(account: str, user: UserRoleUpdate,  collection: Collection):
    admin =  _fetch_user(account, account, account, collection)
    if admin==None:
        raise HTTPException(status_code=404, detail="Admin Not Found")
    elif admin["role"]!="admin":
        raise HTTPException(status_code=403, detail="Not Admin")
    user_to_update  = collection.update_one({"username": user.username}, {"$set": {"role": user.role}})
    if user_to_update.modified_count == 0:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"status": 200}
