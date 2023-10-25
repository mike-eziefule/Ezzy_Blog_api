from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.dependencies import injection
from schema.user_schema import UserCreate, UserLogin, ShowUser
from schema.models import User
# from typing import List


user_route = APIRouter()

@user_route.post('/sign-up', response_model = ShowUser)
def register_user(new_user: UserCreate, db:Session=Depends(injection.get_db)):
    new_user = User(
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        username=new_user.firstname +'.'+ new_user.lastname[0],
        email = new_user.email,
        password = new_user.password,
        # password = Hasher.get_hash_password(new_user.password),
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user



#SIGNING USER TEST
# @user_route.post('/sign-in')
# def login_user(user: UserLogin, db:Session=Depends(injection.get_db)):
#     auth_user = db.query(User).all()
#     for row in auth_user:
#         if row.email == user.email and row.password == user.password:
#             return {"message": "Login successful"}
#     return {"message": "credentials are incorrect"}
