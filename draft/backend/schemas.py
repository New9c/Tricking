from pydantic import BaseModel
from enum import Enum

class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"

class UserResponse(BaseModel):
    username: str
    hashed_pwd: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
