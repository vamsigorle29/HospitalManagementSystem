"""Database models and schemas"""
from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

from database import Base

class Notification(Base):
    __tablename__ = "notifications"
    
    notification_id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    channel = Column(String, nullable=False)  # SMS, EMAIL
    recipient = Column(String, nullable=False)
    message = Column(String, nullable=False)
    notification_metadata = Column("metadata", JSON)  # Use different Python name, same DB column
    sent_at = Column(DateTime(timezone=True), server_default=func.now())

class NotificationCreate(BaseModel):
    event_type: str
    channel: str
    recipient: str
    message: str
    metadata: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None  # For compatibility with appointment service

class NotificationResponse(BaseModel):
    notification_id: int
    event_type: str
    channel: str
    recipient: str
    message: str
    metadata: Optional[Dict[str, Any]]
    sent_at: datetime
    
    class Config:
        from_attributes = True

