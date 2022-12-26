from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from typing import Optional

class BasePost(BaseModel):
    title: str 
    content: str
    published: bool = True




class CreatePost(BasePost):
    pass

class ResponsePost(BaseModel):
    title: str
    content: str
    published: bool


class DemoPost(BaseModel):
    pass
    
class UserResponse(BaseModel):
    id: str
    email: str
    #created_at: datetime

    class Config:
        orm_mode = True

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime
    #owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

class ResponseOut(BaseModel):
    Post: PostResponse
    votes: int


class CreateUser(BaseModel):
    email: EmailStr
    password: str




class UserAuthentication(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class VoteData(BaseModel):
    post_id: int
    vote_direction: int