from jose import jwt
from fastapi import HTTPException, status
from schema.models import User
from database.database import sessionLocal
from typing import Generator

SECRET_KEY = "mysupersecretkey"
ALGORITHM = "HS256"



class reusables_codes:
    #this block of codes recieves an encoded token(which carries some relevant data like email address of the user),
    # decodes it, then returns the username/email address.
    #Afterwards, it performs some validation with the decoded email against the email address on the database
    
    def get_user_from_token(db, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms =[ALGORITHM])
            username:str = payload.get("sub") #"sub" is a field holding the username/email address
            if username is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="Invalid Email credentials")
            
            #Querry the sub(email) from to token against the stored email
            user = db.query(User).filter(User.email==username).first()
            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="User is not authorized")
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Unable to verify credentials")
        
        #if successful, return the user as authenticated, for further processing.
        return user
    
    
    @staticmethod
    def get_db() -> Generator:
        try:
            db = sessionLocal()
            yield db
        finally:
            db.close()