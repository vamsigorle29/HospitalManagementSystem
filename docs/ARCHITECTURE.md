# Hospital Management System - Architecture Documentation

## System Architecture

### Microservices Overview

The HMS is built as a collection of microservices, each responsible for a specific domain:

1. **Patient Service** - Manages patient data and CRUD operations
2. **Doctor Service** - Manages doctor information and scheduling
3. **Appointment Service** - Core booking, rescheduling, cancellation logic
4. **Billing Service** - Bill generation and tax calculation
5. **Prescription Service** - Prescription management
6. **Payment Service** - Payment processing (idempotent)
7. **Notification Service** - Notification delivery

### Database-per-Service Pattern

Each microservice maintains its own database:

```
┌─────────────────────────────────────────────────────────┐
│                    Patient Service                       │
│                  ┌──────────────┐                       │
│                  │  Patient DB   │                       │
│                  └──────────────┘                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                   Doctor Service                         │
│                  ┌──────────────┐                       │
│                  │  Doctor DB    │                       │
│                  └──────────────┘                       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│                 Appointment Service                      │
│                  ┌──────────────┐                       │
│                  │ Appointment DB│                       │
│                  └──────────────┘                       │
└─────────────────────────────────────────────────────────┘
```

## ER Diagrams

### Patient Service Database

```
┌────────────────────┐
│     patients        │
├────────────────────┤
│ patient_id (PK)    │
│ name               │
│ email              │
│ phone              │
│ dob                │
│ created_at         │
└────────────────────┘
```

### Doctor Service Database

```
┌────────────────────┐
│      doctors        │
├────────────────────┤
│ doctor_id (PK)     │
│ name               │
│ email              │
│ phone              │
│ department         │
│ specialization     │
│ created_at         │
└────────────────────┘
```

### Appointment Service Database

```
┌────────────────────┐
│   appointments      │
├────────────────────┤
│ appointment_id(PK) │
│ patient_id (FK*)   │
│ doctor_id (FK*)    │
│ department         │
│ slot_start         │
│ slot_end           │
│ status             │
│ reschedule_count   │
│ created_at         │
└────────────────────┘

* FK references maintained via API calls to other services
```

### Billing Service Database

```
┌────────────────────┐
│       bills         │
├────────────────────┤
│ bill_id (PK)       │
│ patient_id (FK*)   │
│ appointment_id(FK*)│
│ amount             │
│ status             │
│ created_at         │
└────────────────────┘
```

### Prescription Service Database

```
┌────────────────────┐
│  prescriptions     │
├────────────────────┤
│ prescription_id(PK)│
│ appointment_id(FK*)│
│ patient_id (FK*)   │
│ doctor_id (FK*)    │
│ medication         │
│ dosage             │
│ days               │
│ issued_at          │
└────────────────────┘
```

### Payment Service Database

```
┌────────────────────┐
│     payments        │
├────────────────────┤
│ payment_id (PK)    │
│ bill_id (FK*)      │
│ amount             │
│ method             │
│ reference (unique) │
│ paid_at            │
└────────────────────┘
```

### Notification Service Database

```
┌────────────────────┐
│  notifications      │
├────────────────────┤
│ notification_id(PK)│
│ event_type         │
│ channel            │
│ recipient          │
│ message            │
│ metadata (JSON)    │
│ sent_at            │
└────────────────────┘
```

## Context Map

```
┌─────────────┐         ┌──────────────┐
│   Patient    │────────►│              │
│   Service    │         │              │
└─────────────┘         │              │
                       │  Appointment │
┌─────────────┐         │  Service     │
│   Doctor    │────────►│              │
│   Service   │         │              │
└─────────────┘         └──────┬───────┘
                                │
                                ▼
                        ┌──────────────┐
                        │   Billing    │
                        │   Service    │
                        └──────┬───────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   Payment    │
                        │   Service    │
                        └──────┬───────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
        ┌──────────────┐               ┌──────────────┐
        │Prescription  │               │Notification  │
        │Service       │               │Service       │
        └──────────────┘               └──────────────┘
```

## Inter-Service Communication

### Synchronous HTTP Calls

Services communicate via HTTP/REST calls:
- Appointment Service → Patient Service (verify patient)
- Appointment Service → Doctor Service (verify doctor, check department)
- Appointment Service → Billing Service (create bill on completion)
- Appointment Service → Notification Service (send notifications)

### Replicated Read Models

Appointment Service maintains:
- `doctor_department` - cached from Doctor Service for reporting

## Business Rules

### Appointment Booking Rules
1. Minimum 2-hour lead time required
2. Clinic hours: 9 AM to 6 PM
3. Slot duration: 30 minutes
4. Maximum 1 active appointment per patient per time slot
5. Doctor daily cap: 8 appointments per doctor per day
6. Department mismatch rejected

### Reschedule Rules
1. Maximum 2 reschedules per appointment
2. Cannot reschedule within 1 hour of appointment
3. Must maintain 2-hour lead time

### Cancellation Rules
1. >2 hours before: Full refund
2. ≤2 hours before: 50% fee
3. No-show: 100% consultation fee

### Billing Rules
1. 5% tax applied to all bills
2. Bill created automatically on appointment completion
3. Bills can be voided before payment

### Payment Rules
1. Idempotent operations via Idempotency-Key header
2. No double-charging on retries
3. Payment updates bill status to PAID

## Deployment Architecture

### Docker Compose (Local Development)
- Each service runs in its own container
- SQLite databases for simplicity
- Service-to-service communication via container names

### Kubernetes (Production)
- Deployment manifests with resource limits
- Service objects for cluster-internal communication
- Ingress for external access
- Health probes (liveness/readiness)
- Horizontal scaling support

## Monitoring & Observability

### Metrics
- Request rate, latency, error rate per service
- Business metrics: appointments_created, bill_creation_latency, payments_failed

### Logging
- Structured JSON logs
- Correlation ID for request tracing
- PII masking for compliance

### Tracing
- Distributed tracing with correlation IDs
- Request flow visualization

## Security Considerations

### API Security
- PII masking in logs
- Input validation
- SQL injection prevention via ORM

### RBAC (Ready for Implementation)
- Role-based access control framework in place
- Endpoints can be decorated with role requirements
- Roles: reception, doctor, billing, admin

## Scalability

### Horizontal Scaling
- Stateless services (except database)
- Load balancer distributes requests
- Database replication for write scaling

### Caching Strategy
- Appointment Service caches doctor department
- Can be extended with Redis for shared cache

## Technology Stack

- **Framework**: FastAPI (Python)
- **Database**: SQLite (dev), PostgreSQL (prod)
- **ORM**: SQLAlchemy
- **Logging**: Structlog
- **Containerization**: Docker
- **Orchestration**: Kubernetes
- **Communication**: HTTP/REST

