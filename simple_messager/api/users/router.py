from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import text

from simple_messager.api.users.auth import current_user
from simple_messager.apps.users.model import User
from simple_messager.apps.users.schemas import UserSchema, UserUpdate
from simple_messager.db import get_async_session

router_user = APIRouter(
    tags=["Users"],
    prefix="/users",
)


@router_user.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[UserSchema],
)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router_user.get(
    "/{user_id}/",
    status_code=status.HTTP_200_OK,
    response_model=UserSchema,
)
async def get_user_by_id(
    user_id: int, session: AsyncSession = Depends(get_async_session)
):
    query = select(
        User.id,
        User.email,
        User.username,
        User.avatar,
        User.phone_number,
        User.is_active,
        User.is_superuser,
        User.is_verified,
    ).where(User.id == user_id)
    row: CursorResult = await session.execute(query)
    user_row = row.mappings().fetchone()
    if user_row is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = dict(user_row)
    user_schema = UserSchema(**user_dict)
    return user_schema


@router_user.get("/me", response_model=UserSchema)
async def get_current_user(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(
        User.id,
        User.email,
        User.username,
        User.avatar,
        User.phone_number,
        User.is_active,
        User.is_superuser,
        User.is_verified,
    ).where(User.id == user.id)
    row: CursorResult = await session.execute(query)
    user_row = row.mappings().fetchone()
    if user_row is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = dict(user_row)
    user_schema = UserSchema(**user_dict)
    return user_schema


@router_user.put("/me", response_model=UserSchema)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(User).where(User.id == current_user.id)
    result = await session.execute(query)
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    for attr, value in user_update.dict(exclude_unset=True).items():
        setattr(user, attr, value)
    await session.commit()
    await session.refresh(user)
    return user


@router_user.delete(
    "/me",
)
async def delete_current_user(
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    query = select(User).where(User.id == current_user.id)
    result = await session.execute(query)
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}


@router_user.get(
    "/search_user",
    status_code=status.HTTP_200_OK,
    response_model=List[UserSchema],
)
async def search_users(
    search_query: str = Query(..., min_length=1, description="Search query"),
    session: AsyncSession = Depends(get_async_session),
):
    query = text(
        """
        SELECT * 
        FROM users
        WHERE username
        ILIKE :search_query
        """
    )
    rows: CursorResult = await session.execute(
        query, {"search_query": f"%{search_query}%"}
    )
    user_list = []
    for user_row in rows.fetchall():
        user_dict = {
            "id": user_row.id,
            "email": user_row.email,
            "username": user_row.username,
            "avatar": user_row.avatar,
            "phone_number": user_row.phone_number,
            "is_active": user_row.is_active,
            "is_superuser": user_row.is_superuser,
            "is_verified": user_row.is_verified,
        }
        user_schema = UserSchema(**user_dict)
        user_list.append(user_schema)
    return user_list
