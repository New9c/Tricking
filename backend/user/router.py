from typing import Dict
from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient

from user.auth import CurrentLoggedInUser
from user.schemas import Gender, User, UserCreate, UserLogin, UserUpdate
from user.config import config
import user.service as service


uri = f"mongodb+srv://aimccccccccc:{config.PASSWORD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"
# 連接 MongoDB
client = MongoClient(uri)
db = client["ncku_tricking_db"] # 你的資料庫名稱
users_collection = db["users"] # 你的使用者集合名稱

router = APIRouter(
    prefix="/api/v1",
    tags=["User"]
)

core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "User Already Exists"},
    401: {"description": "Invalid Credentials"},
    403: {"description": "Access Denied"},
    404: {"description": "User Not Found"},
}

@router.post("/register", responses=core_responses)
def register_user(user: UserCreate) -> dict:
    service.register_user(user, users_collection)
    return {"status_code": 200}

@router.put("/me", responses=core_responses)
def update_user(username: str, user: UserUpdate) -> dict:
    return service.update_user(username, user, users_collection)

@router.post("/login", responses=core_responses)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return service.login(form_data, users_collection)

@router.post("/delete", responses=core_responses)
def delete_user(account: str):
    service.delete_user(account, users_collection)
    return {"status_code": 200}

@router.get("/me", responses=core_responses)
def fetch_user(username: CurrentLoggedInUser):
    return service.fetch_user(username, users_collection)
