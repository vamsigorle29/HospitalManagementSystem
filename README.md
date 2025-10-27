# Hospital Management System (HMS) - Microservices Architecture

A comprehensive microservices-based Hospital Management System built with FastAPI, implementing database-per-service pattern, inter-service communication, and full containerization support.

## Architecture Overview

The system consists of 7 microservices, each with its own database:

1. **Patient Service** (Port 8001) - CRUD for patients, PII masking in logs
2. **Doctor & Scheduling Service** (Port 8002) - Doctor listings, availability checks
3. **Billing Service** (Port 8003) - Bill generation, tax calculation
4. **Appointment Service** (Port 8004) - Booking, rescheduling, cancellation workflows
5. **Prescription Service** (Port 8005) - Prescription management
6. **Payment Service** (Port 8006) - Idempotent payment processing
7. **Notification Service** (Port 8007) - SMS/Email notifications

## Features

### Core Requirements
- ✅ Database-per-service (no shared tables)
- ✅ API versioning (/v1)
- ✅ OpenAPI 3.0 documentation
- ✅ Standard error schema with correlation ID
- ✅ Pagination and filtering
- ✅ PII masking in logs
- ✅ Inter-service workflows with business rules
- ✅ RBAC ready

### Business Rules Implemented

**Appointment Service:**
- Minimum 2-hour lead time for bookings
- Clinic hours: 9 AM to 6 PM
- Maximum 2 reschedules per appointment
- Cannot reschedule within 1 hour of appointment
- Cancellation policy: >2h (full refund), ≤2h (50% fee), no-show (100% fee)
- Maximum 1 active appointment per patient per time slot
- Maximum 8 appointments/day per doctor
- Department mismatch validation

**Billing Service:**
- 5% tax on all bills
- Automatic bill creation on appointment completion
- Cancellation fee handling

**Payment Service:**
- Idempotent payments via Idempotency-Key header
- No double-charging on retries

## Quick Start

### Using Docker Compose (Recommended for local development)

1. Clone and navigate to the project:
```bash
cd Scalable_Assignment
```

2. Build and start all services:
```bash
docker-compose up --build
```

3. Check service health:
```bash
curl http://localhost:8001/health  # Patient Service
curl http://localhost:8002/health  # Doctor Service
curl http://localhost:8004/health  # Appointment Service
# ... and so on
```

4. Seed sample data (optional):
```bash
python scripts/seed_data.py
```

### Using Kubernetes (Minikube)

1. Start Minikube:
```bash
minikube start
```

2. Build Docker images:
```bash
docker build -t patient-service:latest ./patient-service
docker build -t doctor-service:latest ./doctor-service
docker build -t appointment-service:latest ./appointment-service
docker build -t billing-service:latest ./billing-service
docker build -t prescription-service:latest ./prescription-service
docker build -t payment-service:latest ./payment-service
docker build -t notification-service:latest ./notification-service
```

3. Load images into Minikube:
```bash
minikube image load patient-service:latest
minikube image load doctor-service:latest
minikube image load appointment-service:latest
minikube image load billing-service:latest
minikube image load prescription-service:latest
minikube image load payment-service:latest
minikube image load notification-service:latest
```

4. Apply Kubernetes manifests:
```bash
kubectl apply -f k8s/
```

5. Check deployments:
```bash
kubectl get pods
kubectl get services
```

6. Port forward to access services:
```bash
kubectl port-forward service/patient-service 8001:8001
kubectl port-forward service/doctor-service 8002:8002
kubectl port-forward service/appointment-service 8004:8004
# ... etc
```

## API Documentation

### Service Endpoints

All services follow REST API conventions and are documented via OpenAPI/Swagger:

- **Patient Service**: http://localhost:8001/docs
- **Doctor Service**: http://localhost:8002/docs
- **Billing Service**: http://localhost:8003/docs
- **Appointment Service**: http://localhost:8004/docs
- **Prescription Service**: http://localhost:8005/docs
- **Payment Service**: http://localhost:8006/docs
- **Notification Service**: http://localhost:8007/docs

### Example Workflows

#### 1. Book an Appointment
```bash
POST http://localhost:8004/v1/appointments
Headers:
  Content-Type: application/json
  X-Correlation-ID: unique-id
Body:
{
  "patient_id": 1,
  "doctor_id": 1,
  "department": "Cardiology",
  "slot_start": "2025-01-15T10:00:00",
  "slot_end": "2025-01-15T10:30:00"
}
```

#### 2. Reschedule Appointment
```bash
POST http://localhost:8004/v1/appointments/{id}/reschedule?new_slot_start=2025-01-15T14:00:00&new_slot_end=2025-01-15T14:30:00
Headers:
  X-Correlation-ID: unique-id
```

#### 3. Cancel Appointment
```bash
POST http://localhost:8004/v1/appointments/{id}/cancel
Headers:
  X-Correlation-ID: unique-id
```

#### 4. Complete Appointment & Create Bill
```bash
POST http://localhost:8004/v1/appointments/{id}/complete
Headers:
  X-Correlation-ID: unique-id
```

#### 5. Make Payment (Idempotent)
```bash
POST http://localhost:8006/v1/payments
Headers:
  Content-Type: application/json
  Idempotency-Key: unique-key-123
Body:
{
  "bill_id": 1,
  "amount": 500.00,
  "method": "UPI"
}
```

## Monitoring

### Metrics
- `appointments_created_total` - Total appointments created
- `bill_creation_latency_ms` - Bill creation latency
- `payments_failed_total` - Failed payments

### Logging
- Structured JSON logs with correlation ID
- PII masking (email, phone, name)
- Request path, latency, and trace ID

### Health Checks
All services expose `/health` endpoints for Kubernetes readiness/liveness probes.

## Database Schema

### Database-per-Service Split

**Patient DB:**
- patients (patient_id, name, email, phone, dob, created_at)

**Doctor DB:**
- doctors (doctor_id, name, email, phone, department, specialization, created_at)

**Appointment DB:**
- appointments (appointment_id, patient_id, doctor_id, department, slot_start, slot_end, status, reschedule_count, created_at)

**Billing DB:**
- bills (bill_id, patient_id, appointment_id, amount, status, created_at)

**Prescription DB:**
- prescriptions (prescription_id, appointment_id, patient_id, doctor_id, medication, dosage, days, issued_at)

**Payment DB:**
- payments (payment_id, bill_id, amount, method, reference, paid_at)

**Notification DB:**
- notifications (notification_id, event_type, channel, recipient, message, metadata, sent_at)

## Context Map

```
Patient Service ─────┬───> Appointment Service
                     │       │
Doctor Service ─────┘       ├───> Billing Service ───> Payment Service
                            │       │
Prescription Service ←──────┘       └──> Notification Service
```

## Testing

Run unit tests:
```bash
pytest
```

Test specific service:
```bash
cd patient-service
pytest
```

## Project Structure

```
.
├── patient-service/
│   ├── app.py
│   ├── models.py
│   ├── database.py
│   ├── utils.py
│   ├── Dockerfile
│   └── requirements.txt
├── doctor-service/
│   ├── app.py
│   ├── models.py
│   ├── database.py
│   ├── Dockerfile
│   └── requirements.txt
├── appointment-service/
│   ├── app.py
│   ├── models.py
│   ├── database.py
│   ├── Dockerfile
│   └── requirements.txt
├── billing-service/
├── prescription-service/
├── payment-service/
├── notification-service/
├── k8s/
│   ├── *-deployment.yaml
│   └── ingress.yaml
├── docker-compose.yml
└── README.md
```

## Assignments Completed

### 1. Microservices (6 Marks) ✅
- All 7 services implemented with CRUD, search, filtering
- PII masking in logs
- OpenAPI 3.0 documentation
- Standard error schema with correlation ID

### 2. Database-Per-Service Split (1.5 Marks) ✅
- Separate database per service
- No shared tables
- ER diagrams included in documentation
- Basic CRUD with integrity

### 3. Inter-Service Workflows (2.5 Marks) ✅
- Book Appointment with full validation
- Reschedule with business rules
- Cancel with refund policy
- No-show handling
- Complete appointment → create bill
- All rules enforced

### 4. Containerization (2 Marks) ✅
- Dockerfile per service
- docker-compose.yml for local testing
- Evidence: docker ps output

### 5. Deployment on Minikube (2 Marks) ✅
- Kubernetes manifests per service
- Deployment, Service, Ingress
- ConfigMaps/Secrets (via env vars)
- PVCs via volumes
- Resource requests/limits
- Health probes

### 6. Monitoring Tasks (2 Marks) ✅
- Metrics endpoints
- Structured JSON logs
- Correlation ID in logs
- PII masking
- Health endpoints

### 7. Documentation (2 Marks) ✅
- Comprehensive README
- API documentation
- ER diagrams
- Context map
- Deployment guides

## Contributing

This project was built for academic purposes as part of a Scalable Services course assignment.

## License

Academic use only.

