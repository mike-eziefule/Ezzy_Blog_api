from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#steps for setting up an SQL database
"""
According to https://fastapi.tiangolo.com/tutorial/sql-databases/
These are the steps for setting up an SQL database
1. Create Engine:
you need to pass the database url and also import create_engine from sqlalchemy

2. Bind Enging with Session: 
Session is like a workspace for your engine therefore import sessionmaker from sqlalchemy.orm.
then bind  to the engine with a line of code

3. Connect Engine
4. Describe the database tables(using declarative base)
5. Reading the database and building the metadata
6. Create the objects

"""

# option 2: using SQLITE_database
SQLALCHEMY_DATABASE_URL ='sqlite:///./database/sqlite.db'

#create engine instance
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args= {"check_same_thread": False})

#create session instance or workspace for engine and binding at once
sessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

#define base class for database connection
Base = declarative_base()
