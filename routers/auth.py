from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta
from starlette.status import HTTP_400_BAD_REQUEST

from expense_tracker_backend.core.Oauth import authenticate_user,  create_access_token, get_user
from expense_tracker_backend.core.database import get_session
from expense_tracker_backend.schemas.user import TokenResponse, UserCreate
from expense_tracker_backend.core.utils import get_hashed_password
from expense_tracker_backend.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db : AsyncSession = Depends(get_session)):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})

    access_token_expires = timedelta(minutes=30)
    access_token = await create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/register")
async def register(user_data: UserCreate, db : AsyncSession= Depends(get_session)):
    user = await get_user(db, user_data.email)
    if user :
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User already exists")

    hashed_password = get_hashed_password(user_data.password)

    new_user = User(email= user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "New user added", "user_id": new_user.id}