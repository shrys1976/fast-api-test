
from  datetime import datetime
from pydantic import BaseModel
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


   