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
    # Extract fields, handling both data and metadata
    notif_dict = notification.dict(exclude={'data'}, exclude_unset=True)
    if notification.data and not notif_dict.get('metadata'):
        notif_dict['notification_metadata'] = notification.data
    elif 'metadata' in notif_dict:
        notif_dict['notification_metadata'] = notif_dict.pop('metadata')
    if not notif_dict.get('channel'):
        notif_dict['channel'] = 'EMAIL'  # Default channel
    if not notif_dict.get('recipient'):
        notif_dict['recipient'] = 'unknown'  # Default recipient
    if not notif_dict.get('message'):
        notif_dict['message'] = f"Event: {notif_dict.get('event_type', 'unknown')}"
    
    db_notification = Notification(**notif_dict)
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
    
    # Convert back to response format
    response_dict = {
        "notification_id": db_notification.notification_id,
        "event_type": db_notification.event_type,
        "channel": db_notification.channel,
        "recipient": db_notification.recipient,
        "message": db_notification.message,
        "metadata": db_notification.notification_metadata,
        "sent_at": db_notification.sent_at
    }
    return NotificationResponse(**response_dict)

@app.get("/v1/notifications", response_model=list[NotificationResponse])
def get_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all notifications"""
    notifications = db.query(Notification).offset(skip).limit(limit).all()
    # Map notification_metadata to metadata for response
    result = []
    for notif in notifications:
        result.append(NotificationResponse(
            notification_id=notif.notification_id,
            event_type=notif.event_type,
            channel=notif.channel,
            recipient=notif.recipient,
            message=notif.message,
            metadata=notif.notification_metadata,
            sent_at=notif.sent_at
        ))
    return result

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "notification-service"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8007))
    uvicorn.run(app, host="0.0.0.0", port=port)

