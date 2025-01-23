from typing import Dict
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from pymongo import MongoClient

from user.router import router as user_router
from tricktionary.router import router as tricktionary_router


core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "User Already Exists"},
    401: {"description": "Invalid Credentials"},
    403: {"description": "Access Denied"},
    404: {"description": "User Not Found"},
}
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(tricktionary_router)
