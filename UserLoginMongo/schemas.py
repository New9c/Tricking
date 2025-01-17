from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class User(BaseModel):
    username: str
    email: str
    phone: str
    gender: str
    age: int
    password: str

class UserLogin(BaseModel):
    account: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    phone: str
    gender: str
    age: int
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    password: Optional[str] = None

