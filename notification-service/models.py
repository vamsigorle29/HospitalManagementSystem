"""Database models and schemas"""
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime

from database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    notification_id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    channel = Column(String, nullable=False)  # SMS, EMAIL
    recipient = Column(String, nullable=False)
    message = Column(String, nullable=False)
    metadata = Column(JSON)
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

class NotificationCreate(BaseModel):
    event_type: str
    channel: str
    recipient: str
    message: str
    metadata: dict = None

class NotificationResponse(BaseModel):
    notification_id: int
    event_type: str
    channel: str
    recipient: str
    message: str
    metadata: dict
    sent_at: datetime
    
    class Config:
        from_attributes = True

