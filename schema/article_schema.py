from pydantic import BaseModel, EmailStr
from datetime import date


class Blog(BaseModel):
    title: str
    content: str  = 'Create Magic here'

class BlogCreate(BaseModel):
    content: str  = 'Create Magic here'
class ShowBlog(Blog):
    author: str
    date_posted: date
    class Config:
        orm_mode = True

