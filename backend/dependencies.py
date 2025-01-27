from pymongo import MongoClient
from pymongo.database import Collection
from config import config

URI = f"mongodb+srv://aimccccccccc:{config.PASSWORD}@clusterfluster.jzaut.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFluster"
client = MongoClient(URI)
db = client[config.DB_NAME]

def get_users_collection() -> Collection:
    return db["users"]

def get_tricktionary_collection() -> Collection:
    return db["tricks"]

def mock_users_collection() -> Collection:
    return db["mock_users"]

def mock_tricktionary_collection() -> Collection:
    return db["mock_tricks"]
