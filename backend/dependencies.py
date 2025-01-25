from fastapi import Depends
from pymongo import MongoClient
from pymongo.database import Collection
from config import config

uri = f"mongodb+srv://aimccccccccc:{config.PASSWORD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"
client = MongoClient(uri)
db = client["ncku_tricking_db"]

def get_users_collection() -> Collection:
    return db["users"]

def get_tricktionary_collection() -> Collection:
    return db["tricks"]

def mock_users_collection() -> Collection:
    return db["mock_users"]

def mock_tricktionary_collection() -> Collection:
    return db["mock_tricks"]
