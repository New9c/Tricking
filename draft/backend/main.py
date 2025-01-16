from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from models import User
from schemas import UserResponse, Token
from database import engine, get_db
import service

app = FastAPI()

@app.post("/register", response_model=UserResponse)
def register_user(username: str, password: str, db: Session = Depends(get_db)) -> User:
    return service.register_user(username, password, db)

@app.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    return service.login(username, password, db)
