"""Database models and schemas"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

from database import Base

class Bill(Base):
    __tablename__ = "bills"
    
    bill_id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, nullable=False, index=True)
    appointment_id = Column(Integer, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String, nullable=False, default="OPEN")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BillCreate(BaseModel):
    patient_id: int
    appointment_id: int
    amount: float

class BillUpdate(BaseModel):
    amount: Optional[float] = None
    status: Optional[str] = None

class BillResponse(BaseModel):
    bill_id: int
    patient_id: int
    appointment_id: int
    amount: Decimal
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

