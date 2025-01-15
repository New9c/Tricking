from fastapi import FastAPI

app = FastAPI()

db = [{"item_name": "Item-1"}, {"item_name": "Item-2"}, {"item_name": "Item-3"}]


@app.get("/items")
async def read_item(skip: int = 0, limit: int = 10):
    return db[skip : skip + limit]
# blahblahblah/items?skip=1&limit=1
