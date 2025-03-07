from typing_extensions import Annotated
from pydantic import BaseModel,EmailStr, Field
from pydantic.types import conint
from datetime import datetime
from typing import Optional




class PostBase(BaseModel):
    title:str
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr

    class config:
        orm_mode=True



class Post(PostBase):
    id:int
    owner_id:int
    owner:UserOut

        #to make pydantic model read non dict model as sqlalchemy model
    class config:
        orm_mode=True

class PostOut(BaseModel):
    Post:Post
    votes:int

    class config:
        orm_mode=True


class UserCreate(BaseModel):
    email:EmailStr
    password:str




class UserLogin(BaseModel):
    email:EmailStr
    password:str


class Token(BaseModel):
    access_token:str
    token_type:str


class TokenData(BaseModel):
    id:Optional[int]=None


class Votes(BaseModel):
    post_id:int
    dir:Annotated[int, Field(ge=0, le=1)]
