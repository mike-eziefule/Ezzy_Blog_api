from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index = True)
    firstname = Column(String, nullable= False, index= True)
    lastname = Column(String, nullable= False, index= True)
    nickname = Column(String, nullable= False, index= True)
    email = Column(String, nullable= False, unique=True, index= True)
    password = Column(String, nullable= False, index= True)
    status = Column(String, default= "ACTIVE")
    articles = relationship("Blogs", back_populates = "owner")


class Blogs(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True, index = True)
    title = Column(String, nullable= False, unique=True, index= True)
    content = Column(String, nullable= False)
    author = Column(String, nullable= False)
    date_posted = Column(Date)
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    owner = relationship("User", back_populates = "articles")