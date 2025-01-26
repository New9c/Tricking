from enum import Enum
from pydantic import BaseModel
from typing import Optional

class Role(str, Enum):
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"

class User(BaseModel):
    username: str
    email: str
    phone: str
    gender: Gender
    age: int
    password: str
    role: Role = Role.STUDENT

class UserLogin(BaseModel):
    account: str
    password: str

class UserCreate(BaseModel):
    username: str
    email: str
    phone: str
    gender: Gender
    age: int
    password: str
    role: Role = Role.STUDENT

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    gender: Optional[Gender] = None
    age: Optional[int] = None
    password: Optional[str] = None
    role: Optional[Role] = None

