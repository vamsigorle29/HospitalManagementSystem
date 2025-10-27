"""Database models and schemas"""
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

from database import Base

class Doctor(Base):
    __tablename__ = "doctors"
    
    doctor_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)
    department = Column(String, nullable=False)
    specialization = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class DoctorResponse(BaseModel):
    doctor_id: int
    name: str
    email: EmailStr
    phone: str
    department: str
    specialization: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class SlotAvailability(BaseModel):
    start: str
    end: str

