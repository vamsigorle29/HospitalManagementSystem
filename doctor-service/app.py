"""
Doctor & Scheduling Service - Doctor listings, availability checks
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Optional
import structlog

from database import get_db, init_db
from models import Doctor, Schedule, SlotAvailability, DoctorResponse

logger = structlog.get_logger()

app = FastAPI(title="Doctor Service", version="v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clinc hours configuration
CLINIC_HOURS_START = 9  # 9 AM
CLINIC_HOURS_END = 18   # 6 PM
SLOT_DURATION_MINUTES = 30

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/v1/doctors", response_model=List[DoctorResponse])
def get_doctors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    department: Optional[str] = None,
    specialization: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all doctors with optional filtering"""
    query = db.query(Doctor)
    
    if department:
        query = query.filter(Doctor.department == department)
    
    if specialization:
        query = query.filter(Doctor.specialization == specialization)
    
    total = query.count()
    doctors = query.offset(skip).limit(limit).all()
    
    logger.info("doctors_retrieved", total=total, returned=len(doctors))
    return doctors

@app.get("/v1/doctors/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor by ID"""
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    
    if not doctor:
        logger.warning("doctor_not_found", doctor_id=doctor_id)
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    logger.info("doctor_retrieved", doctor_id=doctor_id)
    return doctor

@app.get("/v1/doctors/{doctor_id}/availability")
def check_availability(
    doctor_id: int,
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    """Check availability for a doctor on a specific date"""
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    # Query appointment service to get booked slots
    # For now, we'll return all available slots
    request_date = datetime.strptime(date, "%Y-%m-%d").date()
    
    # Get today's date
    today = datetime.now().date()
    
    # Check if date is valid
    if request_date < today:
        raise HTTPException(status_code=400, detail="Cannot book in the past")
    
    # Get existing appointments for this doctor on this date
    # This would require cross-service communication with appointment service
    # For now, we'll return all slots as available
    
    slots = generate_slots_for_date(request_date)
    
    logger.info("availability_checked", doctor_id=doctor_id, date=date, slots_available=len(slots))
    return {
        "doctor_id": doctor_id,
        "date": date,
        "available_slots": slots,
        "clinic_hours": {"start": f"{CLINIC_HOURS_START}:00", "end": f"{CLINIC_HOURS_END}:00"}
    }

@app.get("/v1/doctors/{doctor_id}/department")
def get_doctor_department(doctor_id: int, db: Session = Depends(get_db)):
    """Get doctor's department (for validation)"""
    doctor = db.query(Doctor).filter(Doctor.doctor_id == doctor_id).first()
    
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    return {"doctor_id": doctor_id, "department": doctor.department}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "doctor-service"}

def generate_slots_for_date(date):
    """Generate all possible slots for a given date"""
    slots = []
    start_time = datetime.combine(date, datetime.min.time().replace(hour=CLINIC_HOURS_START))
    end_time = datetime.combine(date, datetime.min.time().replace(hour=CLINIC_HOURS_END))
    
    current = start_time
    while current < end_time:
        slot_end = current + timedelta(minutes=SLOT_DURATION_MINUTES)
        slots.append({
            "start": current.strftime("%Y-%m-%dT%H:%M:%S"),
            "end": slot_end.strftime("%Y-%m-%dT%H:%M:%S")
        })
        current = slot_end
    
    return slots

