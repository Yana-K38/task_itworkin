from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from fastapi_users import FastAPIUsers
from simple_messager.api.auth.db import User
from simple_messager.api.auth.manager import get_user_manager

import os
from dotenv import load_dotenv

cookie_transport = CookieTransport(cookie_max_age=3600)


load_dotenv()

SECRET = os.getenv("SECRET")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user()