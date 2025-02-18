from pymongo.collection import Collection
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from collections import defaultdict
import user.error as Error

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
    if '@' in username or ' ' in username:
        return False
    return True

def _verify_email(email: str|None)-> bool:
    if email==None:
        return True
    if '@' in email:
        return True
    return False

def _verify_phone(phone: str|None)-> bool:
    if phone==None:
        return True
    for char in phone:
        if not char.isdigit():
            return False
    return True

def _verify_params(user: UserCreate|UserUpdate):
    if not _verify_username(user.username) or not _verify_age(user.age) or not _verify_email(user.email) or not _verify_phone(user.phone):
        raise Error.INVALID_PARAMETERS

def _create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire_time = datetime.now(timezone.utc) + timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    access_token = jwt.encode(to_encode, key=config.SECRET_JWT, algorithm=config.ALGORITHM)
    return access_token

def _fetch_user(check_username, check_email, check_phone, collection: Collection):
    user = collection.find_one({"username": check_username, "password": {"$ne": ""}})
    if user==None:
        user = collection.find_one({"email": check_email, "password": {"$ne": ""}})
    if user==None:
        user = collection.find_one({"phone": check_phone, "password": {"$ne": ""}})
    return user

def fetch_user(username, collection: Collection):
    user = collection.find_one({"username": username})
    if user==None:
        raise Error.USER_NOT_FOUND
    user.pop("_id")
    return user

def login(form_data: OAuth2PasswordRequestForm, collection: Collection):
    # check username, email and phone with account
    user = UserLogin(account=form_data.username, password=form_data.password)
    if user.password!="":
        login_user = _fetch_user(user.account, user.account, user.account, collection)
    else:
        login_user = collection.find_one({"username": user.account, "password": ""})

    if login_user==None:
        raise Error.USER_NOT_FOUND
    if not _verify_pwd(user.password, login_user["password"]):
        raise Error.PASSWORD_INVALID
    access_token = _create_access_token(data={"sub": login_user["username"]})
    return {"role": login_user["role"], "access_token": access_token, "token_type": "bearer"}

def register_user(user: UserCreate, collection: Collection):
    """
    Will try to register a user using a UserCreate class and a database.
    Fails if the username, email or phone number is taken.
    """
    if user.password!="" and _fetch_user(user.username, user.email, user.phone, collection)!=None:
        raise Error.USER_ALREADY_EXISTS
    _verify_params(user)

    if user.password!="":
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
            raise Error.USER_NOT_FOUND
        else:
            return {"status_code": 200}
    else:
        return {"status_code": 200, "msg": "No Data Updated"}

def delete_user(account: str, collection: Collection):
    user_to_delete= _fetch_user(account, account, account, collection)

    if user_to_delete==None:
        raise Error.USER_NOT_FOUND
    collection.delete_one({"username": user_to_delete["username"]})


def admin_fetch_users(account: str, collection: Collection):
    admin = _fetch_user(account, account, account, collection)
    if admin == None:
        raise Error.ADMIN_NOT_FOUND
    elif admin["role"] != Role.ADMIN:
        raise Error.NOT_ADMIN
    users = collection.find({ "role": { "$ne": Role.ADMIN } })
    group = defaultdict(set)
    for user in users:
        group[user["role"]].add(user["username"])
    group_json = {}
    role_order = [Role.TEACHER, Role.STUDENT_ADVANCED, Role.STUDENT_BEGINNER]
    for role in role_order:
        if role in group:
            group_json[role] = group[role]
    return group_json


def admin_update_user_role(account: str, user: UserRoleUpdate,  collection: Collection):
    admin = _fetch_user(account, account, account, collection)
    if admin == None:
        raise Error.ADMIN_NOT_FOUND
    elif admin["role"] != Role.ADMIN:
        raise Error.NOT_ADMIN
    user_to_update = collection.update_one({"username": user.username}, {"$set": {"role": user.role}})
    if user_to_update.modified_count == 0:
        raise Error.USER_NOT_FOUND
    return {"status": 200}
