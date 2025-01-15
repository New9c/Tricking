from fastapi import FastAPI
from routers.api_v1.routers import router

app = FastAPI()

app.include_router(router, prefix="/api/v1")
