import uvicorn
from fastapi import FastAPI

# from src.api.users.router import router_user

from fastapi_users import fastapi_users, FastAPIUsers

from fastapi import FastAPI

from simple_messager.api.auth.auth import auth_backend
from simple_messager.apps.users.models import User
from simple_messager.api.auth.manager import get_user_manager
from simple_messager.apps.users.schemas import UserCreate, UserRead



app = FastAPI(
    title = "Simple messenger APP",
    docs_url="/docs",
    redoc_url="/redoc",
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)




if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
    )