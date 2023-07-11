# models\models.py
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey


metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "user_info"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


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

