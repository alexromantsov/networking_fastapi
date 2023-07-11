# auth\routes.py
from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from auth.base_config import auth_backend
from auth.manager import get_user_manager
from auth.schemas import UserCreate, UserRead

router = APIRouter()

fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend],
)

# Маршруты аутентификации JWT
auth_router = fastapi_users.get_auth_router(auth_backend)

# Маршруты регистрации
register_router = fastapi_users.get_register_router(UserRead, UserCreate)


router.include_router(
    auth_router,
    # prefix="/jwt",

)

router.include_router(
    register_router,
    # prefix="/register",
)
