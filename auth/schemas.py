# auth\schemas.py
import uuid
from typing import Optional
from fastapi_users import schemas
from pydantic import EmailStr, Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    username: str = Field(..., description="Уникальное имя пользователя.")
    email: EmailStr = Field(..., description="Адрес электронной почты пользователя.")
    password: str = Field(..., description="Пароль пользователя.")
    is_active: Optional[bool] = Field(True, description="Состояние активации учетной записи пользователя.")
    is_superuser: Optional[bool] = Field(False, description="Является ли пользователь суперпользователем.")
    is_verified: Optional[bool] = Field(False, description="Подтвержден ли аккаунт пользователя.")


class UserUpdate(schemas.BaseUserUpdate):
    pass
