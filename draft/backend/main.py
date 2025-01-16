from typing import Dict
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from schemas import Gender
from database import get_db
import service

core_responses: Dict = {
    200: {"description": "Success"},
    400: {"description": "User Already Existant"},
    401: {"description": "Invalid Credentials"},
    404: {"description": "User Not Found."},
}
app = FastAPI()

@app.post("/register", responses=core_responses)
def register_user(
        username: str, 
        pwd: str, 
        email: str,
        phone_num: str,
        age: int,
        gender: Gender,
        db: Session = Depends(get_db),
    ) -> dict:
    service.register_user(username, pwd, email, phone_num, age, gender, db)
    return {"status_code": 200}

@app.post("/update", responses=core_responses)
def update_user(
        uid: str, 
        username: str|None = None, 
        pwd: str|None = None,
        email: str|None = None,
        phone_num: str|None = None,
        age: int|None = None,
        gender: Gender|None = None,
        db: Session = Depends(get_db),
    ) -> dict:
    service.update_user(uid, username, pwd, email, phone_num, age, gender, db)
    return {"status_code": 200}

@app.post("/login", responses=core_responses)
def login(account: str, password: str, db: Session = Depends(get_db)):
    service.login(account, password, db)
    return {"status_code": 200}

@app.post("/delete", responses=core_responses)
def delete_user(uid: str, db: Session = Depends(get_db)):
    service.delete_user(uid, db)
    return {"status_code": 200}

@app.get("/get", responses=core_responses)
def fetch_user(uid: str, db: Session = Depends(get_db)):
    return service.fetch_user(uid, db)
