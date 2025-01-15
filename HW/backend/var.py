from fastapi import FastAPI

app = FastAPI()


@app.get("/{userId}")
async def root(userId):
    return {"message": f"{userId} is a werid number"}
