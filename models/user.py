from datetime import datetime
from sqlmodel import Field,SQLModel

class User(SQLModel, table=True):
    id : int |  Field(default=None,  primary_key=True, index=True)
    email : str |  Field(default=None,  unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

