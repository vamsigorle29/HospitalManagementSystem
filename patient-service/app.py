"""
Patient Service - CRUD operations for patients
"""
from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
import structlog
from datetime import datetime
from typing import List, Optional
from database import get_db, init_db
from models import Patient, PatientCreate, PatientUpdate, PatientResponse
from utils import mask_pii

# Structured logging with PII masking
logger = structlog.get_logger()

app = FastAPI(title="Patient Service", version="v1")

# CORS middleware
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

@app.get("/v1/patients", response_model=List[PatientResponse])
def get_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    name: Optional[str] = None,
    phone: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all patients with optional filtering"""
    query = db.query(Patient)
    
    if name:
        query = query.filter(Patient.name.ilike(f"%{name}%"))
    
    if phone:
        query = query.filter(Patient.phone.ilike(f"%{phone}%"))
    
    total = query.count()
    patients = query.offset(skip).limit(limit).all()
    
    # Log with PII masking
    logger.info(
        "patients_retrieved",
        total=total,
        returned=len(patients),
        filters={"name": mask_pii("name", name), "phone": mask_pii("phone", phone)}
    )
    
    return patients

@app.get("/v1/patients/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    """Get patient by ID"""
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    if not patient:
        logger.warning("patient_not_found", patient_id=patient_id)
        raise HTTPException(status_code=404, detail="Patient not found")
    
    logger.info("patient_retrieved", patient_id=patient_id)
    return patient

@app.post("/v1/patients", response_model=PatientResponse, status_code=201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    """Create a new patient"""
    # Check for existing email
    existing = db.query(Patient).filter(Patient.email == patient.email).first()
    if existing:
        logger.warning("patient_exists", email=mask_pii("email", patient.email))
        raise HTTPException(status_code=400, detail="Patient with this email already exists")
    
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    
    logger.info(
        "patient_created",
        patient_id=db_patient.patient_id,
        name=mask_pii("name", db_patient.name)
    )
    
    return db_patient

@app.put("/v1/patients/{patient_id}", response_model=PatientResponse)
def update_patient(
    patient_id: int,
    patient: PatientUpdate,
    db: Session = Depends(get_db)
):
    """Update patient"""
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    if not db_patient:
        logger.warning("patient_not_found", patient_id=patient_id)
        raise HTTPException(status_code=404, detail="Patient not found")
    
    for key, value in patient.dict(exclude_unset=True).items():
        setattr(db_patient, key, value)
    
    db.commit()
    db.refresh(db_patient)
    
    logger.info("patient_updated", patient_id=patient_id)
    return db_patient

@app.delete("/v1/patients/{patient_id}", status_code=204)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    """Delete patient (soft delete - just mark as inactive)"""
    db_patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    # In a real system, you might want to check for active appointments
    db.delete(db_patient)
    db.commit()
    
    logger.info("patient_deleted", patient_id=patient_id)
    return None

@app.get("/v1/patients/{patient_id}/exists")
def check_patient_exists(patient_id: int, db: Session = Depends(get_db)):
    """Check if patient exists"""
    exists = db.query(Patient).filter(Patient.patient_id == patient_id).first() is not None
    return {"exists": exists}

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "patient-service"}

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)

