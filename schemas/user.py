from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

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