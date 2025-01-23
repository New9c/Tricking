from typing import Dict
from fastapi import APIRouter
from pymongo import MongoClient

from tricktionary.schemas import TrickCreate, TrickDelete
from tricktionary.config import config
import tricktionary.service as service

uri = f"mongodb+srv://aimccccccccc:{config.PASSWORD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&routerName=ClusterFluster"
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

router = APIRouter(
    prefix="/api/v1/tricktionary",
    tags=["Tricktionary"]
)

@router.get("/get", responses=core_responses)
def fetch_tricks() -> dict:
    return service.fetch_tricks(tricks_collection)

@router.post("/add", responses=core_responses)
def add_trick(trick: TrickCreate) -> dict:
    service.add_trick(trick, tricks_collection)
    return {"status_code": 200}

@router.delete("/delete", responses=core_responses)
def delete_trick(trick: TrickDelete):
    service.delete_trick(trick, tricks_collection)
    return {"status_code": 200}
