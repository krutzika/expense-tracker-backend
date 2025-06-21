from fastapi import Depends
from typing import Annotated, AsyncGenerator
from .config import Settings
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker

settings = Settings()

connect_args = {"check_same_thread": False}

engine: AsyncEngine = create_async_engine(settings.DATABASE_URL, echo=True, connect_args=connect_args)

async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

