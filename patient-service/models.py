"""Database models and schemas"""
from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.sql import func
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime

# SQLAlchemy Model
from database import Base

class Patient(Base):
    __tablename__ = "patients"
    
    patient_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Pydantic Schemas
class PatientBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    dob: date

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    dob: Optional[date] = None

class PatientResponse(PatientBase):
    patient_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

