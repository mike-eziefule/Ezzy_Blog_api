from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from service.Blog_services import reusables_codes
from schema.models import User, Blogs
from schema.article_schema import ShowBlog
from typing import List



admin_route = APIRouter()

##USERS
#admin view aLL users
@admin_route.get('/users/all_users')
async def get_all_users(db:Session=Depends(reusables_codes.get_db)):
    all_users = db.query(User).all()
    return all_users


# #admin delete a user by their id address
@admin_route.delete('/users/delete/{id:int}')
async def delete_user(id:int, db:Session = Depends(reusables_codes.get_db)):
    existing_user = db.query(User).filter(User.id==id)
    if not existing_user.first():
        return {"message": "User no found"}
    existing_user.delete()
    db.commit()
    return {
        'message':'User delete successfully',
    }


#admin delete all user
@admin_route.delete('/users/delete/all')
async def delete_all_users(db:Session=Depends(reusables_codes.get_db)):
    user = db.query(User).all()
    if user == []:
        return {"message": "User Database is empty"}

    for user in user:
        db.delete(user)
        db.commit()
    db.close()
    return {"message": "All users successfully deleted"}


#ARTICLES
#admin view aLL articles
@admin_route.get('/articles/view_all')
async def get_all_articles(db:Session=Depends(reusables_codes.get_db)):
    all_blogs = db.query(Blogs).all()
    return all_blogs

#FILTER ARTICLES BY AUTHOR ID
@admin_route.get("/{user_id}", response_model= List[ShowBlog])
async def list_blog_from_author(user_id, db:Session = Depends(reusables_codes.get_db)):
    articles = db.query(Blogs).filter(Blogs.owner_id == user_id)
    if not articles.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='No articles from this user')
    
    return articles

#admin view aLL articles
@admin_route.delete('/articles/delete_all')
async def delete_all_articles(db:Session=Depends(reusables_codes.get_db)):
    all_blogs = db.query(Blogs).all()
    for blog in all_blogs:
        db.delete(blog)
        db.commit()
    db.close()
    return {"message": "All Articles successfully deleted"}
    