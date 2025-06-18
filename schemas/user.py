from pydantic import BaseModel, EmailStr

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
