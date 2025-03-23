from re import S
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

# defining schema with pydantic so that user don't post anything unnecessary


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Post(PostBase):
    # this will return only title, content and published info to the user when he create/update post
    # agr user ko koi aur detail bhi dikhani hai jo PostBase ka hissa nhi to wo mein yahan define krdonga
    # like id: int
    id: int
    created_at: datetime
    owner: UserOut  # to return the info of user when retrieving a post. Note that UserOut should be above this class because python will interpret top to bottom

    class Config:
        from_attributes = (
            True  # ye na kiya to value return krty hoe dict ka error ayega
        )


class PostOut(BaseModel):
    Post: Post  # this is referencing the class Post above
    votes: int

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    # '...' will make sure that input is required, le 1 means that input is less than or equals to 1
    dir: int = Field(..., le=1)
