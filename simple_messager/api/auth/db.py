from typing import AsyncGenerator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base


from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
# from simple_messager.apps.users.model import User
from sqlalchemy import Boolean, Column, Integer, String


Base: DeclarativeMeta = declarative_base()

from simple_messager.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    avatar = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)



engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
    
