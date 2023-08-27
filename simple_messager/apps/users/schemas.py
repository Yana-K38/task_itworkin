import uuid

from fastapi_users import schemas
from pydantic import BaseModel
from datetime import datetime
from fastapi_users import schemas
from typing import Optional
from pydantic.types import UUID


class UserRead(BaseModel):
    email: str
    username: str
    avatar: Optional[str] = None
    phone_number: Optional[str] = None


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserRegister(BaseModel):
    email: str
    username: str


class UserSchema(UserRead):
    uuid: UUID
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    created_at: datetime
    updated_at: datetime

