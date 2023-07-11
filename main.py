from fastapi import FastAPI, Depends
from auth.routes import router as auth_router
from auth.database import User
from message.routes import router as message_router
from auth.base_config import fastapi_users
from message.descriptions import *

app = FastAPI(
    title="Networking App",
    openapi_tags=TAGS_METADATA
)

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Регистрация и авторизация"]
)

app.include_router(
    message_router,
    prefix="/api/message",
    tags=["Сообщения"]
)


@app.get("/")
async def root(user: User = Depends(fastapi_users.current_user(optional=True))):
    if user:
        return {"message": f"Привет, {user.username}"}
    else:
        return {"message": "Привет, незнакомец, для продолжения нужно авторизоваться"}
