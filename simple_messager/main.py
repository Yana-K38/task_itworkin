import uvicorn
from fastapi import FastAPI, Depends

from simple_messager.api.users.auth import auth_backend, current_user, fastapi_users
from simple_messager.db import User
from simple_messager.apps.users.schemas import UserCreate, UserRead

from simple_messager.api.users.router import router_user
from simple_messager.api.chat.router import router
from pathlib import Path
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


app = FastAPI(
    title="Simple messenger APP",
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
app.include_router(router)


templates = Jinja2Templates(directory=Path(__file__).resolve().parent / "templates")


@app.get("/chat")
def get_chat_page(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="localhost",
        port=8000,
    )
