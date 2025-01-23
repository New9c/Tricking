from pymongo.collection import Collection
from fastapi import HTTPException
from schemas import TrickCreate, TrickDelete
from collections import defaultdict

def fetch_tricks(collection: Collection):
    tricks = collection.find()
    group = defaultdict(set)
    for trick in tricks:
        group[trick["level"]].add(trick["name"])
    group_json = {level: list(names) for level, names in group.items()}
    return group_json

def add_trick(trick: TrickCreate, collection: Collection):
    trick_to_create= collection.find_one({"name": trick.name})
    if trick_to_create!=None:
        raise HTTPException(status_code=400, detail="Trick Already Exists")
    collection.insert_one(trick.model_dump())

def delete_trick(trick: TrickDelete, collection: Collection):
    trick_to_delete = collection.find_one({"name": trick.name})
    if trick_to_delete==None:
        raise HTTPException(status_code=404, detail="Trick Not Found")
    collection.delete_one({"name": trick.name})
