from pydantic import BaseModel, EmailStr
from datetime import date


class Blog(BaseModel):
    title: str
    content: str  = 'Create Magic here'

class ShowBlog(Blog):
    date_posted: date
    # author: str
    # author: 
    class Config:
        orm_mode = True

class BlogCreate(Blog):
    pass

    class Config:
        orm_mode = True