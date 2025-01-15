from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/ithome")
async def root():
    return {"message": "ironman 2023"}

@app.get("/user")
async def root():
    return {"message": "ck642509"}
