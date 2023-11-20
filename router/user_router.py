from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from service.Blog_services import reusables_codes
from schema.user_schema import UserCreate, EditUser, ShowUser
from schema.models import User
from router.login_router import oauth2_scheme


user_route = APIRouter()

#USER REGISTRATION ROUTE
@user_route.post('/sign-up', response_model = ShowUser)
async def register_user(new_user: UserCreate, db:Session=Depends(reusables_codes.get_db)):

    emails = db.query(User).all()
    for row in emails:
        if row.email == new_user.email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Email already in use")
        if row.nickname == new_user.nickname:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Nickname already in use, Try another nickname")
    
    new_user = User(
        firstname=new_user.firstname,
        lastname=new_user.lastname,
        nickname= new_user.nickname,
        email = new_user.email,
        password = new_user.password,
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


#EDITING USER INFORMATION BY User ONLY
@user_route.put("/update/{id}")
async def Edit_User_Info(id:int, input:EditUser, db:Session = Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    existing_user = db.query(User).filter(User.id==id)
    if not existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with:{id} does not exist"
        )
    
    if existing_user.first().id == user.id:
        # db update reqires a dict input but input:BlogCreate is a pydantic model hence the use of jsonable encoder to convert it
        # existing_article = existing_article.update(jsonable_encoder(input))  
        existing_user.update(input.__dict__)                    #Alternatively
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Information updated successfully'
        )

    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Profile can only be EDITED by Owner'
        )

#DELETE MY ACCOUNT Owner ONLY
@user_route.delete("/delete/{id}")
async def Delete_My_account(id:int, password:str, db:Session=Depends(reusables_codes.get_db), token:str=Depends(oauth2_scheme)):
    
    #authentication
    user = reusables_codes.get_user_from_token(db, token)
    
    existing_user = db.query(User).filter(User.id==id)
    if not existing_user.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with:{id} does not exist"
        )
    
    if existing_user.first().id == user.id and user.password == password:
        existing_user.delete()                   #Alternatively
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED, 
            detail='Account deleted successfully'
        )
    raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail= 'Account Owner\'s permission required'
        )