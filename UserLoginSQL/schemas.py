from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class User(BaseModel):
    username: str
    email: str
    phone: str
    gender: Gender
    age: int
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    phone: str
    gender: Gender
    age: int
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    password: Optional[str] = None
