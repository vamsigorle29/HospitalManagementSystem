"""
Payment Service - Handle payments with idempotency
"""
from fastapi import FastAPI, HTTPException, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import structlog

from database import get_db, init_db
from models import Payment, PaymentCreate, PaymentResponse

logger = structlog.get_logger()

app = FastAPI(title="Payment Service", version="v1")

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

@app.post("/v1/payments", response_model=PaymentResponse, status_code=201)
def create_payment(
    payment: PaymentCreate,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
    db: Session = Depends(get_db)
):
    """Create a payment (idempotent operation)"""
    # Check if payment with this idempotency key already exists
    existing = db.query(Payment).filter(Payment.reference == idempotency_key).first()
    if existing:
        logger.info("payment_already_exists", idempotency_key=idempotency_key)
        return existing
    
    db_payment = Payment(**payment.dict())
    db_payment.reference = idempotency_key
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    
    logger.info(
        "payment_created",
        payment_id=db_payment.payment_id,
        bill_id=payment.bill_id,
        amount=payment.amount,
        reference=idempotency_key
    )
    
    return db_payment

@app.get("/v1/payments", response_model=list[PaymentResponse])
def get_payments(
    skip: int = 0,
    limit: int = 100,
    bill_id: int = None,
    db: Session = Depends(get_db)
):
    """Get payments"""
    query = db.query(Payment)
    
    if bill_id:
        query = query.filter(Payment.bill_id == bill_id)
    
    payments = query.offset(skip).limit(limit).all()
    return payments

@app.get("/v1/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    """Get payment by ID"""
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    return payment

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "payment-service"}

