from typing import List
from pydantic import BaseModel, Field, validator

from forbidden_words import forbidden_words


class Users(BaseModel):
    username: str = Field(..., max_length=20, min_length=2,
                          description='The username of the article should not be less than 2 and more than 20 characters and and contain only letters')
    email: str = Field(..., max_length=50, min_length=2,
                       description='The name of the article should not be less than 2 and more than 50 characters and contain @')
    password: str = Field(..., max_length=20, min_length=8,
                          description='The name of the article should not be less than 2 and more than 20 characters')


    @validator('email')
    def check_email(cls, v):
        if '.' and '@' in v:
            return v

    @validator('password')
    def check_password(cls, v):
        punctuation_marks = ['.', ',', ':', ';', '"', '{', '}', '[', ']', '!', '@', '#', '<', '>', '(', ')', '*', '^',
                             '%', '$', '&', '?', '№']
        cur_list = []
        if not v.islower():
            for i in v:
                if i.isdigit():
                    cur_list.append(i)
                    break
            for i in punctuation_marks:
                if i in v:
                    cur_list.append(i)
                    break
        if len(cur_list) == 2:
            return v


class Tags(BaseModel):
    id: int
    tags: str


class UploadPost(BaseModel):
    title: str = Field(..., max_length=50, min_length=3,
                       description='The title of the article should not be less than 3 and more than 50 characters')
    description: str = Field(..., max_length=1500, min_length=3,
                             description='The description of the article should not be less than 3 and more than 1500 characters')

    tags: List[str] = None

    username: str

    id: int = None

    @validator('description', 'title')
    def check_description(cls, v):
        for word in forbidden_words:
            if word in v:
                raise ValueError('В описании не должно быть мата')
        return v


class GetPost(BaseModel):
    id: int
    title: str
    description: str



class GetUser(BaseModel):
    id: int
    username: str
    email: str


class User(BaseModel):
    username: str



class TokenPayload(BaseModel):
    user_id: int = None


