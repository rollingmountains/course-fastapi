from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

import psycopg2 as db
import psycopg2.extras 
import time

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to run a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# connecting with DB directly using postgres driver
'''
while True:

    try:
        conn = db.connect(host='localhost', database='fastapi', user='postgres', password='Tiram@123') 
        cursor = conn.cursor(cursor_factory= psycopg2.extras.RealDictCursor)
        print('Successful DB connection')
        break
    except Exception as error:
        print('DB connection failed')
        print('Error: ', error)
        time.sleep(2)
        '''