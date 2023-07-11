# message\schemas.py
from pydantic import BaseModel, Field
from datetime import datetime


class MessageCreate(BaseModel):
    content: str = Field(..., description="Содержимое создаваемого сообщения.")


class MessageBase(BaseModel):
    content: str


class MessageRead(MessageBase):
    id: int = Field(..., description="Идентификатор сообщения.")
    user_id: int = Field(..., description="Идентификатор пользователя, создавшего сообщение.")
    created_at: datetime = Field(..., description="Время создания сообщения.")
    updated_at: datetime = Field(..., description="Время последнего обновления сообщения.")

    class Config:
        orm_mode = True


class MessageUpdate(BaseModel):
    content: str = Field(..., description="Новое содержимое сообщения.")

