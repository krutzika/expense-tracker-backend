from datetime import datetime, timedelta, timezone
from typing import Optional, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select
from sqlmodel.ext.asyncio.session import AsyncSession
from expense_tracker_backend.schemas.user import UserInDB
from expense_tracker_backend.core.utils import verify_password

from expense_tracker_backend.core.config import Settings
from expense_tracker_backend.core.database import get_session
from expense_tracker_backend.models.user import User

settings = Settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_user (db: AsyncSession, email : str) -> Optional[User]:
    user = await db.exec(select(User).where(User.email == email))
    return user.first()

async def authenticate_user(db: AsyncSession, email : str, password : str):
    user = await get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

async def create_access_token(data : dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else :
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user (token : Annotated[str, Depends(oauth2_scheme)], db: AsyncSession = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try :
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id= payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await db.get(User, user_id)
    if user is None:
        raise credentials_exception
    return user
