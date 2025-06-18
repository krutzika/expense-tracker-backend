from fastapi import Depends
from typing import Annotated
from .config import Settings
from sqlmodel import SQLModel, Session, create_engine

settings = Settings()

connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

