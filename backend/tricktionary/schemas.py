from pydantic import BaseModel

class Trick(BaseModel):
    name: str
    level: str

class TrickCreate(BaseModel):
    name: str
    level: str

class TrickDelete(BaseModel):
    name: str
