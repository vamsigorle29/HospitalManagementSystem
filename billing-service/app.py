"""
Billing Service - Bill generation, tax calculation, cancellation handling
"""
from fastapi import FastAPI, HTTPException, Depends, Query, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
import structlog
from uuid import uuid4

from database import get_db, init_db
from models import Bill, BillCreate, BillUpdate, BillResponse

logger = structlog.get_logger()

app = FastAPI(title="Billing Service", version="v1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

TAX_RATE = 0.05  # 5% tax

@app.on_event("startup")
async def startup():
    init_db()

@app.post("/v1/bills", response_model=BillResponse, status_code=201)
def create_bill(
    bill: BillCreate,
    correlation_id: str = Header(None),
    db: Session = Depends(get_db)
):
    """Create a new bill"""
    if not correlation_id:
        correlation_id = str(uuid4())
    
    # Check for existing bill for this appointment
    existing = db.query(Bill).filter(Bill.appointment_id == bill.appointment_id).first()
    if existing:
        logger.warning("bill_exists", appointment_id=bill.appointment_id)
        raise HTTPException(status_code=400, detail="Bill already exists for this appointment")
    
    # Calculate with tax
    base_amount = bill.amount
    tax = base_amount * TAX_RATE
    total_amount = base_amount + tax
    
    db_bill = Bill(
        patient_id=bill.patient_id,
        appointment_id=bill.appointment_id,
        amount=total_amount,
        status="OPEN"
    )
    
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    
    logger.info(
        "bill_created",
        bill_id=db_bill.bill_id,
        appointment_id=bill.appointment_id,
        amount=total_amount,
        correlation_id=correlation_id
    )
    
    return db_bill

@app.post("/v1/bills/{bill_id}/void")
def void_bill(
    bill_id: int,
    correlation_id: str = Header(None),
    db: Session = Depends(get_db)
):
    """Void a bill (for cancellations)"""
    if not correlation_id:
        correlation_id = str(uuid4())
    
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    if bill.status == "PAID":
        raise HTTPException(status_code=400, detail="Cannot void a paid bill")
    
    bill.status = "VOID"
    db.commit()
    
    logger.info("bill_voided", bill_id=bill_id, correlation_id=correlation_id)
    return bill

@app.get("/v1/bills", response_model=List[BillResponse])
def get_bills(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    patient_id: Optional[int] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get bills with filters"""
    query = db.query(Bill)
    
    if patient_id:
        query = query.filter(Bill.patient_id == patient_id)
    
    if status:
        query = query.filter(Bill.status == status)
    
    total = query.count()
    bills = query.order_by(Bill.created_at.desc()).offset(skip).limit(limit).all()
    
    logger.info("bills_retrieved", total=total, returned=len(bills))
    return bills

@app.get("/v1/bills/{bill_id}", response_model=BillResponse)
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get bill by ID"""
    bill = db.query(Bill).filter(Bill.bill_id == bill_id).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    return bill

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "billing-service"}

