from fastapi_users import schemas
from pydantic import BaseModel
from fastapi_users import schemas
from typing import Optional

class UserRead(schemas.BaseUser[int]):
    id: int
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


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    email: str
    avatar: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: bool
    is_superuser: bool
    is_verified: bool


class UserRegister(BaseModel):
    email: str
    username: str


class UserSchema(UserRead):
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
