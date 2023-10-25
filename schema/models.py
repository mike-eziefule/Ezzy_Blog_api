from database.database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index = True)
    firstname = Column(String, nullable= False, index= True)
    lastname = Column(String, nullable= False, index= True)
    username = Column(String, nullable= False, unique=True, index= True)
    email = Column(String, nullable= False, unique=True, index= True)
    password = Column(String, nullable= False, index= True)
    status = Column(Boolean, default= True)
    articles = relationship("Blogs", back_populates = "author")


class Blogs(Base):
    __tablename__ = 'articles'
    
    id = Column(Integer, primary_key=True, index = True)
    title = Column(String, nullable= False, unique=True, index= True)
    content = Column(String, nullable= False)
    date_posted = Column(Date)
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates = "articles")