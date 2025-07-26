from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    # Existing fields you have...

    sessions = relationship("ConversationSession", back_populates="user")

class ConversationSession(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", order_by="Message.timestamp")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    sender = Column(String(10))  # "user" or "ai"
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    session = relationship("ConversationSession", back_populates="messages")
