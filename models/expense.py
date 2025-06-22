from sqlmodel import Field, SQLModel
from typing import Optional
from enum import Enum
from datetime import datetime

class Category(str, Enum):
    BILLS = "bills"
    GROCERY = "grocery"
    ENTERTAINMENT = "entertainment"
    FOOD_DRINK = "food/drink"
    TRANSPORT = "transport"
    HEALTH = "health"
    OTHER = "other"

class Expense(SQLModel, table=True):
    id : Optional[int] = Field(default=None, primary_key=True)
    user_id : int = Field(foreign_key="user.id")
    amount : float
    description : str
    category : Category
    created_at : datetime = Field(default_factory=datetime.utcnow)