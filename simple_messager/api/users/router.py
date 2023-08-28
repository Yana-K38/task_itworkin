from fastapi import APIRouter, status

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from simple_messager.apps.users.model import User
from simple_messager.apps.users.schemas import UserSchema, UserUpdate
from simple_messager.api.auth.db import get_async_session
from sqlalchemy.future import select
from sqlalchemy.engine.cursor import CursorResult

from simple_messager.api.auth.auth import current_user

router_user= APIRouter(
    tags=["Users"],
    prefix="/users",
)

@router_user.get("/", status_code=status.HTTP_200_OK, response_model=List[UserSchema],)
async def get_all_users(session: AsyncSession = Depends(get_async_session)):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router_user.get("/{user_id}/", status_code=status.HTTP_200_OK, response_model=UserSchema,)
async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(
        User.id, User.email, User.username, User.avatar,
        User.phone_number, User.is_active, User.is_superuser, User.is_verified
        ).where(User.id==user_id)
    row: CursorResult = await session.execute(query)
    user_row=row.mappings().fetchone()
    if user_row is None:
        raise HTTPException(status_code=404, detail="User not found")
    user_dict = dict(user_row)
    user_schema = UserSchema(**user_dict)
    return user_schema


@router_user.get("/me", response_model=UserSchema)
async def get_current_user(user: User = Depends(current_user), session: AsyncSession = Depends(get_async_session)):
    query = select(
        User.id, User.email, User.username, User.avatar,
        User.phone_number, User.is_active, User.is_superuser, User.is_verified
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
    session: AsyncSession = Depends(get_async_session)
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


@router_user.delete("/me",)
async def delete_current_user(
    current_user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).where(User.id == current_user.id)
    result = await session.execute(query)
    user = result.scalar()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    await session.delete(user)
    await session.commit()
    return {"message": "User deleted successfully"}
