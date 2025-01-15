from fastapi import FastAPI

app = FastAPI()


@app.get("/fuck/")
async def root():
    return {"message": "Hello World"}
