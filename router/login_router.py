from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from service.Blog_services import reusables_codes
from sqlalchemy.orm import Session
from schema.models import User
from jose import jwt
from core.config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login/token")


login_route = APIRouter()

@login_route.post("/token")
async def retrieve_token_after_authentication(form_data: OAuth2PasswordRequestForm = Depends(), db:Session=Depends(reusables_codes.get_db)):

    auth_user = db.query(User).all()
    
    for row in auth_user:
        if row.email == form_data.username and row.password == form_data.password:
            data = {'sub': form_data.username}
            jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
            return {"access_token": jwt_token, "token_type": "bearer"}
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="invalid credentials"
        )
    
    