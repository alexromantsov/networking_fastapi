# message\database.py
from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey

from auth.database import Base


class Message(Base):
    __tablename__ = "messages_info"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_info.id"))
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)


class Like(Base):
    __tablename__ = "likes_info"

    user_id = Column(Integer, ForeignKey("user_info.id"), primary_key=True)
    message_id = Column(Integer, ForeignKey("messages_info.id"), primary_key=True)
