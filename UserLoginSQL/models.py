import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from database import engine
from schemas import Gender

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    uid         = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username   = Column(String(50), unique=True, index=True, nullable=False)
    hashed_pwd = Column(String(100), nullable=False)
    email      = Column(String(100), unique=True, index=True, nullable=False)
    phone_num  = Column(String(50), unique=True, index=True, nullable=False)
    age        = Column(Integer, index=True, nullable=False)
    gender     = Column(SQLEnum(Gender), index=True, nullable=False)
    def to_dict(self):
        return {
        "uid"         : self.uid,
        "username"   : self.username,
        "hashed_pwd" : self.hashed_pwd,
        "email"      : self.email,
        "phone_num"  : self.phone_num,
        "age"        : self.age,
        "gender"     : self.gender
        }


Base.metadata.create_all(engine)
