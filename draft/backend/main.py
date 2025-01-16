from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from schemas import Gender
from database import get_db
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

@app.post("/login")
def login(username: str, password: str, db: Session = Depends(get_db)):
    return service.login(username, password, db)
