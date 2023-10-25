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


#Blog Metedata
description = """
### OVERVIEW
* This is a blogging app. The fundamental concept is that 
anyone visiting the website should be able to read a blog 
post written by them or another user.
*  The Blog application should have
a user authentication where a user can create an account and login so that they could be able to
create a blog, also the Blog should have the logout ability.
* Created on October 2023
"""

contact = {
    'name': 'Michael Eziefule',
    'Student ID': 'ALT/SOE/022/5063',
    'email': 'mike.eziefule@gmail.com',
    'github': 'https://github.com/mike-eziefule'
}


tags = [
    {'name': 'Home',
    'description': 'Welcome page route'
    },
    {'name': 'Users',
    'description': 'This are the users related routes'
    },
    {'name': 'Articles',
    'description': 'This are the Articles related routes'
    },
    {'name': 'Admin',
    'description': 'This are the Administrators routes'
    },
    {'name': 'Login',
    'description': 'Login routes'
    }
]

#read metadata, and instructing it to create tables using base schema.
Base.metadata.create_all(bind=engine)

#FastAPI Matadata.
app = FastAPI(  title='Ezzy Blog', 
                description = description,
                contact= contact,
                version= '0.0.1',
                openapi_tags= tags
)

app.include_router(user_route, prefix='/user', tags=['Users'])
app.include_router(blog_route, prefix='/article', tags=['Articles'])
app.include_router(admin_route, prefix='/admin', tags=['Admin'])
app.include_router(login_route, prefix='/login', tags=['Login'])


#view aLL articles
@app.get('/view_all', tags=['Home'], response_model= List[ShowBlog])
def get_all_articles(db:Session=Depends(reusables_codes.get_db)):
    all_blogs = db.query(Blogs).all()
    return all_blogs