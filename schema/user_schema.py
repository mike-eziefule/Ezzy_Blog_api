from pydantic import EmailStr, BaseModel
from schema.article_schema import Blog

class BaseUser(BaseModel):
    email : EmailStr
class UserLogin(BaseUser):
    password : str
class UserCreate(UserLogin):
    firstname: str
    lastname: str
    nickname: str
class EditUser(BaseModel):
    firstname: str
    lastname: str
class ShowUser(UserCreate):
    id : int
    class Config:
        orm_mode = True