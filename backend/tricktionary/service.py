from pymongo.collection import Collection
from collections import defaultdict

import tricktionary.error as Error
from tricktionary.schemas import TrickCreate

def fetch_tricks(collection: Collection):
    tricks = collection.find()
    group = defaultdict(dict)
    for trick in tricks:
        group[trick["level"]][trick["name"]] = trick["desc"]
    group_json = {level: vals for level, vals in group.items()}
    return group_json

def add_trick(trick: TrickCreate, collection: Collection):
    trick_to_create = collection.find_one({"name": trick.name})
    if trick_to_create!=None:
        raise Error.TRICK_ALREADY_EXISTS
    collection.insert_one(trick.model_dump())

def delete_trick(trick: str, collection: Collection):
    trick_to_delete = collection.find_one({"name": trick})
    if trick_to_delete==None:
        raise Error.TRICK_NOT_FOUND
    collection.delete_many({"name": trick})

