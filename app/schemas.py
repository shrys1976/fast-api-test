
from  datetime import datetime
from tokenize import String
from pydantic import BaseModel, EmailStr
from sqlalchemy import Boolean


class PostBase(BaseModel):
    title: str
    content : str
    published : bool  = True

 # db schema
class Post(PostBase):
    id: int
    created_at : datetime
    # title: str
    # content : str
    # published : bool  = True
   
    class Config:
         orm_mode = True    


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email : EmailStrstr
    password: str


class UserOut(BaseModel):
    id : int
    email: EmailStr

    class Config:
            orm_mode = True