from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
from fastapi import FastAPI
db_url = "postgresql://postgres:12345@localhost:5432/Book_Management"

engine = create_engine(db_url)

Base = declarative_base()
maker = sessionmaker(autoflush=False,autocommit =False,bind=engine)

app = FastAPI()

def get_db():
    db = maker()
    try:
        yield db
    finally:
        db.close()