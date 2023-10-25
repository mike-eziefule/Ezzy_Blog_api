from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.Blog_services import reusables_codes
from schema.models import User, Blogs



admin_route = APIRouter()

##USERS
#admin view aLL users
@admin_route.get('/users/all_users')
def get_all_users(db:Session=Depends(reusables_codes.get_db)):
    all_users = db.query(User).all()
    return all_users

# #admin find a user by their id
# @admin_route.get('/users/{id:int}')
# def get_a_user(id:int, db:Session=Depends(reusables_codes.get_db)):
#     user = db.query(User).get(id)
#     if not user:
#         return "No such user"
#     return user

# #admin delete a user by their id address
# @admin_route.delete('/users/delete/{id:int}')
# def delete_user(id:int, db:Session = Depends(reusables_codes.get_db)):
#     existing_user = db.query(User).filter(User.id==id)
#     if not existing_user.first():
#         return {"message": "User no found"}
#     existing_user.delete()
#     db.commit()
#     return {
#         'message':'User delete successfully',
#     }


#admin delete all user
@admin_route.delete('/users/delete/all')
def delete_all_users(db:Session=Depends(reusables_codes.get_db)):
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
def get_all_articles(db:Session=Depends(reusables_codes.get_db)):
    all_blogs = db.query(Blogs).all()
    return all_blogs

#admin view one articles
# @admin_route.delete("/delete/{id}")
# async def delete_article(id:int, db:Session = Depends(reusables_codes.get_db)):
#     existing_article = db.query(Blogs).filter(Blogs.id==id)
#     if not existing_article.first():
#         return {'message':f'Article id:{id} not found'}
#     existing_article.delete() 
#     db.commit()
#     return {
#         'message':'article delete successfully',
#     }

#admin view aLL articles
@admin_route.delete('/articles/delete_all')
def delete_all_articles(db:Session=Depends(reusables_codes.get_db)):
    all_blogs = db.query(Blogs).all()
    for blog in all_blogs:
        db.delete(blog)
        db.commit()
    db.close()
    return {"message": "All Articles successfully deleted"}
    