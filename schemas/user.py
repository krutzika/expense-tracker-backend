from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Dict

from expense_tracker_backend.models.expense import Category

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id : int
    email : EmailStr
    created_at : datetime

    class Config:
        orm_mode = True

class TokenResponse(BaseModel):
    access_token : str
    token_type : str = 'bearer'

class TokenData(BaseModel):
    username : str

class UserInDB(UserCreate):
    hashed_password : str

class  ExpenseCreate(BaseModel):
    amount : float
    description : str
    category : Category
    created_at : Optional[datetime]

class ExpenseRead(BaseModel):
    id: int
    amount : float
    description : str
    category : Category
    created_at : datetime

    class Config:
        orm_mode=True
        from_attributes= True

class ExpenseUpdate(BaseModel):
    amount : Optional[int] = None
    description : Optional[str] = None
    category : Optional[Category] = None
    created_at : Optional[datetime]

class CategoryBreakdown(BaseModel):
    total: float
    percent: float

class ExpenseStatsResponse(BaseModel):
    total_spent: float
    by_category: Dict[str, CategoryBreakdown]

    class Config:
        orm_mode = True



class CategoryTotals(BaseModel):
    total: float


class ComparisonPeriod(BaseModel):
    label: str  # e.g., "Previous 30 Days"
    totals: Dict[str, CategoryTotals]  # category -> total


class ExpenseComparisonResponse(BaseModel):
    current_period: ComparisonPeriod
    previous_period: ComparisonPeriod