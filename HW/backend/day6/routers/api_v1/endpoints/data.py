from fastapi import APIRouter

router = APIRouter()

@router.get("/data")
async def rooter():
    return {"message": "Hello World"}

@router.post("/data")
async def root():
    return {"message": "Hello World"}
