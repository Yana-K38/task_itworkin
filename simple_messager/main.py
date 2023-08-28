import uvicorn
from fastapi import FastAPI, Depends

from simple_messager.api.auth.auth import auth_backend, current_user, fastapi_users
from simple_messager.api.auth.db import User
from simple_messager.apps.users.schemas import UserCreate, UserRead


from simple_messager.apps.users.model import User

from simple_messager.api.users.router import router_user


app = FastAPI(
    title = "Simple messenger APP",
    docs_url="/docs",
    redoc_url="/redoc",
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

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_user)

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
    )