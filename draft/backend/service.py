from fastapi import FastAPI, Depends, HTTPException, status
from models import User
from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(original_pwd: str) -> str:
    return _pwd_context.hash(original_pwd)
def verify_password(checked_pwd: str, hashed_pwd: str):
    return _pwd_context.verify(checked_pwd, hashed_pwd)

def check_user_password_is_correct(db, username, pwd)-> User:
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(pwd, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
