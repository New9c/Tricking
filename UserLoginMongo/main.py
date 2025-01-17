from typing import Dict
from fastapi import FastAPI
from pymongo import MongoClient

from schemas import Gender, User, UserCreate, UserLogin, UserUpdate
import service

PWD = "2G1ix1hjDHtvn2Qt"
uri= f"mongodb+srv://aimccccccccc:{PWD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"

# 連接 MongoDB
client = MongoClient(uri)
db = client["ncku_tricking_db"] # 你的資料庫名稱
users_collection = db["users"] # 你的使用者集合名稱

core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "User Already Exists"},
    401: {"description": "Invalid Credentials"},
    404: {"description": "User Not Found"},
}
app = FastAPI(prefix="/api/v1/")

@app.post("/register", responses=core_responses)
def register_user(user: UserCreate) -> dict:
    service.register_user(user, users_collection)
    return {"status_code": 200}
"""
@app.post("/update", responses=core_responses)
def update_user(user: UserUpdate) -> dict:
    service.update_user(user, users_collection)
    return {"status_code": 200}
"""

@app.post("/login", responses=core_responses)
def login(user: UserLogin):
    service.login(user, users_collection)
    return {"status_code": 200}

@app.post("/delete", responses=core_responses)
def delete_user(account: str):
    service.delete_user(account, users_collection)
    return {"status_code": 200}

@app.get("/get", responses=core_responses)
def fetch_user(account: str):
    return service.fetch_user(account, users_collection)
