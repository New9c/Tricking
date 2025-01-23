from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient

from schemas import TrickCreate, TrickDelete
from config import config
import service

uri = f"mongodb+srv://aimccccccccc:{config.PASSWORD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"
# 連接 MongoDB
client = MongoClient(uri)
db = client["ncku_tricking_db"] # 你的資料庫名稱
tricks_collection = db["tricks"] # 你的使用者集合名稱



core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "trick Already Exists"},
    401: {"description": "Invalid Credentials"},
    403: {"description": "Access Denied"},
    404: {"description": "trick Not Found"},
}
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/tricktionary/get", responses=core_responses)
def fetch_tricks() -> dict:
    return service.fetch_tricks(tricks_collection)

@app.post("/api/v1/tricktionary/add", responses=core_responses)
def add_trick(trick: TrickCreate) -> dict:
    service.add_trick(trick, tricks_collection)
    return {"status_code": 200}

@app.delete("/api/v1/tricktionary/delete", responses=core_responses)
def delete_trick(trick: TrickDelete):
    service.delete_trick(trick, tricks_collection)
    return {"status_code": 200}
