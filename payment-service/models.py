"""Database models and schemas"""
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

from database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    payment_id = Column(Integer, primary_key=True, index=True)
    bill_id = Column(Integer, nullable=False, index=True)
    amount = Column(Numeric(10, 2), nullable=False)
    method = Column(String, nullable=False)
    reference = Column(String, unique=True, index=True)
    paid_at = Column(DateTime(timezone=True), server_default=func.now())

class PaymentCreate(BaseModel):
    bill_id: int
    amount: float
    method: str

class PaymentResponse(BaseModel):
    payment_id: int
    bill_id: int
    amount: Decimal
    method: str
    reference: str
    paid_at: datetime
    
    class Config:
        from_attributes = True

