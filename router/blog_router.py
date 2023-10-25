from fastapi import APIRouter, Depends, HTTPException, status
from service.Blog_services import reusables_codes
from sqlalchemy.orm import Session
from schema.article_schema import ShowBlog, BlogCreate
from schema.models import Blogs
from datetime import datetime
from typing import List
from router.login_router import oauth2_scheme

SECRET_KEY = "mysupersecretkey"
ALGORITHM = "HS256"

blog_route = APIRouter()

@blog_route.get("/{user_id}", response_model= List[ShowBlog])
async def list_blog_from_author(user_id, db:Session = Depends(reusables_codes.get_db)):
    articles = db.query(Blogs).filter(Blogs.author_id == user_id)
    if not articles or articles == []:
        return {'message':f'Article id:{user_id} not found'}
    return articles

@blog_route.post("/create", response_model=ShowBlog)
async def create_article(article:BlogCreate, db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    user = reusables_codes.get_user_from_token(db, token)

    new_article = Blogs(**article.dict(),date_posted = datetime.now().date(), author_id = user.id)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

#EDITING A BLOG
@blog_route.put("/update/{id}")
async def Edit_article(id:int, input:BlogCreate, db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    user = reusables_codes.get_user_from_token(db, token)
    
    existing_article = db.query(Blogs).filter(Blogs.id==id)
    if not existing_article.first():
        return {'message':f'Article id:{id} not found'}
    
    if existing_article.first().author_id == user.id:
        # db update reqires a dict input but input:BlogCreate is a pydantic model hence the use of jsonable encoder to convert it
        # existing_article = existing_article.update(jsonable_encoder(input))  
        existing_article.update(input.__dict__ )                    #Alternatively
        db.commit()
        return {
            'message':'article updated successfully',
            'details':input
        }
    return {
        'Errors':'You are not authorized',
        'message':'Articles Can only be Edited by the Creator'
    }

@blog_route.delete("/delete/{id}")
async def delete_article(id:int, db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    user = reusables_codes.get_user_from_token(db, token)
    
    existing_article = db.query(Blogs).filter(Blogs.id==id)
    if not existing_article.first():
        return {'message':f'Article id:{id} not found'}
    
    if existing_article.first().author_id == user.id:
        existing_article.delete() 
        db.commit()
        return {
            'message':'Your article was delete successfully',
        }
    return {
            'Errors':'You are not authorized',
            'message':'Articles Can only be deleted by the Creators'
        }
