from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from datetime import timedelta

from expense_tracker_backend.core.Oauth import authenticate_user,  create_access_token
from expense_tracker_backend.core.database import get_session
from expense_tracker_backend.schemas.user import TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db : Session = Depends(get_session)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return TokenResponse(access_token=access_token, token_type="bearer")
