from enum import Enum
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from models import User
from schemas import UserResponse, Token, Gender
from database import engine, get_db
import service

app = FastAPI()

@app.post("/register")
def register_user(
        username: str, 
        pwd: str, 
        email: str,
        phone_num: str,
        age: int,
        gender: Gender,
        db: Session = Depends(get_db),
    ) -> dict:
    return service.register_user(username, pwd, email, phone_num, age, gender, db)

@app.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    return service.login(username, password, db)
