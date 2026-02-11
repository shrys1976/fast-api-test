from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base




SQLALCHEMY_DB_URL = 'postgresql://postgres:shrys@localhost/py-api-test'
engine = create_engine(SQLALCHEMY_DB_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally : db.close()   

# application of ORM, doesnt require sql commands, we can control 
# db with python itself

