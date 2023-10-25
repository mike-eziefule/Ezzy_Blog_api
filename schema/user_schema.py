from pydantic import EmailStr, BaseModel
from schema.article_schema import Blog


class BaseUser(BaseModel):
    # username: str
    email : EmailStr

class UserCreate(BaseUser):
    firstname: str
    lastname: str
    password : str

class UserLogin(BaseModel):
    email : EmailStr
    password : str

class ShowUser(BaseUser):
    username: str
    id : int
    
    class Config:
        orm_mode = True