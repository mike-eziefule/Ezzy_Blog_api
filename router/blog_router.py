from fastapi import APIRouter, Depends, HTTPException, status
from service.Blog_services import reusables_codes
from sqlalchemy.orm import Session
from schema.article_schema import ShowBlog, BlogCreate, Blog
from schema.models import Blogs
from datetime import datetime
from router.login_router import oauth2_scheme
from typing import List

blog_route = APIRouter()

#CREATE A NEW ARTICLE
@blog_route.post("/create", response_model= ShowBlog)
async def create_article(title: str, article:BlogCreate, db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    user = reusables_codes.get_user_from_token(db, token)                                       #authorization
    
    new_article = Blogs(title = title, **article.dict(), date_posted = datetime.now().date(), owner_id = user.id, author = user.firstname+' '+user.lastname)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    raise HTTPException(
            status_code=status.HTTP_201_CREATED, 
            detail='article created successfully',
        )
    
    
#FILTER ARTICLES BY AUTHOR ID
@blog_route.get("/view_blogs", response_model= List[ShowBlog])
async def view_my_blog_posts(db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    user = reusables_codes.get_user_from_token(db, token)           #authorization

    articles = db.query(Blogs).filter(Blogs.owner_id == user.id)
    if not articles.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No articles from this user')
    
    return articles

#EDITING AN ARTICLE BY Author ONLY
@blog_route.put("/update/{id}")
async def Edit_my_article(id:int, input:Blog, db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    user = reusables_codes.get_user_from_token(db, token)           #authorization
    
    existing_article = db.query(Blogs).filter(Blogs.id==id)
    if not existing_article.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Article id:{id} does not exist"
        )
    
    if existing_article.first().owner_id == user.id:
        # db update reqires a dict input but input:BlogCreate is a pydantic model hence the use of jsonable encoder to convert it
        # existing_article = existing_article.update(jsonable_encoder(input))  
        existing_article.update(input.__dict__ )  #Alternatively
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='article updated successfully'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'An article can only be EDITED by its Authors'
        )


#DELETE AN ARTICLE BY Author ONLY
@blog_route.delete("/delete/{id}")
async def delete_article(id:int, password:str, db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    user = reusables_codes.get_user_from_token(db, token)      #authorization
    
    existing_article = db.query(Blogs).filter(Blogs.id==id)
    if not existing_article.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Article id:{id} does not exist")
    
    if existing_article.first().owner_id == user.id and user.password == password:
        existing_article.delete() 
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='article deleted successfully',
            )
        
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'This article can only be DELETED by authenticated Authors'
        )
