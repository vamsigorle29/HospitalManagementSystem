"""
Notification Service - SMS/Email notifications
"""
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Dict, Any
import structlog

from database import get_db, init_db
from models import Notification, NotificationCreate, NotificationResponse

logger = structlog.get_logger()

app = FastAPI(title="Notification Service", version="v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/v1/notifications", response_model=NotificationResponse, status_code=201)
def send_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    """Send a notification"""
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    
    # Log notification (in real system, would send SMS/Email)
    logger.info(
        "notification_sent",
        notification_id=db_notification.notification_id,
        event_type=notification.event_type,
        channel=notification.channel
    )
    
    # Simulate sending notification
    print(f"[{notification.channel}] {notification.event_type}: {notification.message}")
    
    return db_notification

@app.get("/v1/notifications", response_model=list[NotificationResponse])
def get_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all notifications"""
    notifications = db.query(Notification).offset(skip).limit(limit).all()
    return notifications

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "notification-service"}

