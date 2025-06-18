from pydantic import BaseModel, EmailStr
from datetime import datetime

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