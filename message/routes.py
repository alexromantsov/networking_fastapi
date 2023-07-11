# message\routes.py
from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from auth.base_config import fastapi_users
from auth.database import User, get_async_session
from message.database import Message, Like
from message.schemas import MessageCreate, MessageRead, MessageUpdate
from message.descriptions import *


router = APIRouter()


@router.post("/", summary=CREATE_MESSAGE_SUMMARY, description=CREATE_MESSAGE_DESCRIPTION)
async def create_message(
        message: MessageCreate,
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_users.current_user(active=True, optional=False))):
    new_message = Message(content=message.content, user_id=current_user.id)
    db.add(new_message)
    await db.commit()
    return {"message": "Сообщение создано"}


@router.get("/", response_model=List[MessageRead],
            summary=GET_ALL_MESSAGES_SUMMARY, description=GET_ALL_MESSAGES_DESCRIPTION)
async def get_messages(
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_users.current_user())):
    result = await db.execute(select(Message))
    messages = result.scalars().all()
    return messages


@router.get("/{message_id}", response_model=MessageRead,
            summary=GET_MESSAGE_SUMMARY, description=GET_MESSAGE_DESCRIPTION)
async def get_message(
        message_id: int = Path(..., description="ID сообщения, которое нужно получить."),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_users.current_user())):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail=MESSAGE_NOT_FOUND)
    return message


@router.put("/{message_id}", summary=UPDATE_MESSAGE_SUMMARY, description=UPDATE_MESSAGE_DESCRIPTION)
async def update_message(
        message_update: MessageUpdate,
        message_id: int = Path(..., description="ID сообщения, которое требуется обновить."),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_users.current_user())):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalars().first()
    if not message:
        raise HTTPException(status_code=404, detail=MESSAGE_NOT_FOUND)
    if message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Чужое сообщение. Нет прав на редактирование")
    message.content = message_update.content
    await db.commit()
    return {"message": "Сообщение изменено"}


@router.delete("/{message_id}", summary=DELETE_MESSAGE_SUMMARY, description=DELETE_MESSAGE_DESCRIPTION)
async def delete_message(
        message_id: int = Path(..., description="ID сообщения, которое требуется удалить."),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_users.current_user())):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalars().first()  # получить первый результат
    if not message:
        raise HTTPException(status_code=404, detail=MESSAGE_NOT_FOUND)
    if message.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Чужое сообщение. Нет прав на удаление")
    await db.delete(message)
    await db.commit()
    return {"message": "Сообщение удалено"}


@router.post("/{message_id}/like", summary=LIKE_MESSAGE_SUMMARY, description=LIKE_MESSAGE_DESCRIPTION)
async def like_message(
        message_id: int = Path(..., description="ID сообщения, которое требуется лайкнуть."),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_users.current_user(active=True, optional=False))):
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalar_one_or_none()
    if not message:
        raise HTTPException(status_code=404, detail="Сообщение для Like не найдено")
    if message.user_id == current_user.id:
        raise HTTPException(status_code=403, detail="Нельзя лайкать собственные сообщения")

    # Проверяем, существует ли уже "лайк" от данного пользователя
    result = await db.execute(
        select(Like).where(Like.user_id == current_user.id, Like.message_id == message_id))
    existing_like = result.scalar_one_or_none()
    if existing_like:
        raise HTTPException(status_code=400, detail="Like уже поставлен")

    like = Like(user_id=current_user.id, message_id=message_id)
    db.add(like)
    await db.commit()
    return {"message": "Like поставлен"}


@router.delete("/{message_id}/like", summary=UNLIKE_MESSAGE_SUMMARY, description=UNLIKE_MESSAGE_DESCRIPTION)
async def unlike_message(
        message_id: int = Path(..., description="ID сообщения, с которого требуется убрать лайк."),
        db: AsyncSession = Depends(get_async_session),
        current_user: User = Depends(fastapi_users.current_user(active=True, optional=False))):
    result = await db.execute(select(Like).where(Like.message_id == message_id, Like.user_id == current_user.id))
    like = result.scalar_one_or_none()
    if not like:
        raise HTTPException(status_code=404, detail="Like не найден")
    await db.delete(like)
    await db.commit()
    return {"message": "Like отменен"}

