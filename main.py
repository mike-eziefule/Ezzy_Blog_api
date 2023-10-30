from fastapi import FastAPI, Depends
from service.Blog_services import reusables_codes
from sqlalchemy.orm import Session
from schema.models import Base, Blogs
from database.database import engine
from router.user_router import user_route
from router.blog_router import blog_route
from router.admin_router import admin_route
from router.login_router import login_route
from schema.article_schema import ShowBlog
from typing import List
from core.config import setting

#read metadata, and instructing it to create tables using base schema.
Base.metadata.create_all(bind=engine)

#FastAPI Matadata.
app = FastAPI(  
    title = setting.TITLE, 
    description = setting.DESCRIPTION,
    contact= setting.CONTACT,
    version= setting.VERSION,
    openapi_tags= setting.TAGS
)

app.include_router(user_route, prefix='/user', tags=['Users'])
app.include_router(blog_route, prefix='/article', tags=['Articles'])
app.include_router(login_route, prefix='/login', tags=['Login'])
app.include_router(admin_route, prefix='/admin', tags=['Admin'])


#view aLL articles
@app.get('/view_all', tags=['Home'], response_model= List[ShowBlog])
def get_all_articles(db:Session=Depends(reusables_codes.get_db)):
    all_blogs = db.query(Blogs).all()
    return all_blogs