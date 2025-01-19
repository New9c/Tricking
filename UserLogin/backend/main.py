from typing import Dict
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from auth import CurrentLoggedInUser
from schemas import Gender, User, UserCreate, UserLogin, UserUpdate
from config import config
import service

uri = f"mongodb+srv://aimccccccccc:{config.PASSWORD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"
# 連接 MongoDB
client = MongoClient(uri)
db = client["ncku_tricking_db"] # 你的資料庫名稱
users_collection = db["users"] # 你的使用者集合名稱



core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "User Already Exists"},
    401: {"description": "Invalid Credentials"},
    403: {"description": "Access Denied"},
    404: {"description": "User Not Found"},
}
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/register", responses=core_responses)
def register_user(user: UserCreate) -> dict:
    service.register_user(user, users_collection)
    return {"status_code": 200}

@app.post("/api/v1/update", responses=core_responses)
def update_user(username: str, user: UserUpdate) -> dict:
    return service.update_user(username, user, users_collection)

@app.post("/api/v1/login", responses=core_responses)
def login(user: UserLogin):
    return service.login(user, users_collection)

@app.post("/api/v1/delete", responses=core_responses)
def delete_user(account: str):
    service.delete_user(account, users_collection)
    return {"status_code": 200}

@app.get("/api/v1/me", responses=core_responses)
def fetch_user(username: CurrentLoggedInUser):
    return service.fetch_user(username, users_collection)
