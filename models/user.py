from expense_tracker_backend.core.database import Base
from sqlmodel import Field, Session, SQLModel, create_engine

class User(SQLModel, table=True):
    id : int |  Field(default=None,  primary_key=True, index=True)
    email : str |  Field(default=None,  unique=True, nullable=False)
    password = str |  Field(default=None,  unique=True, nullable=False)
    created_at :

