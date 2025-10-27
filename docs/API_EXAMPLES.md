# API Usage Examples

## Patient Service

### Create Patient
```bash
curl -X POST http://localhost:8001/v1/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "dob": "1990-01-15"
  }'
```

### Get All Patients (with pagination)
```bash
curl "http://localhost:8001/v1/patients?skip=0&limit=10"
```

### Search Patients
```bash
# Search by name
curl "http://localhost:8001/v1/patients?name=John"

# Search by phone
curl "http://localhost:8001/v1/patients?phone=123456"
```

### Get Patient by ID
```bash
curl http://localhost:8001/v1/patients/1
```

## Doctor Service

### Get All Doctors
```bash
curl http://localhost:8002/v1/doctors
```

### Filter by Department
```bash
curl "http://localhost:8002/v1/doctors?department=Cardiology"
```

### Check Availability
```bash
curl "http://localhost:8002/v1/doctors/1/availability?date=2025-01-15"
```

## Appointment Service

### Book Appointment
```bash
curl -X POST http://localhost:8004/v1/appointments \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: abc-123" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "department": "Cardiology",
    "slot_start": "2025-01-20T10:00:00",
    "slot_end": "2025-01-20T10:30:00"
  }'
```

### Get Appointments
```bash
# All appointments
curl http://localhost:8004/v1/appointments

# By patient
curl "http://localhost:8004/v1/appointments?patient_id=1"

# By doctor
curl "http://localhost:8004/v1/appointments?doctor_id=1"

# By status
curl "http://localhost:8004/v1/appointments?status=SCHEDULED"
```

### Reschedule Appointment
```bash
curl -X POST "http://localhost:8004/v1/appointments/123/reschedule" \
  -H "X-Correlation-ID: reschedule-123" \
  -d '{
    "new_slot_start": "2025-01-20T14:00:00",
    "new_slot_end": "2025-01-20T14:30:00"
  }'
```

### Cancel Appointment
```bash
curl -X POST http://localhost:8004/v1/appointments/123/cancel \
  -H "X-Correlation-ID: cancel-123"
```

### Complete Appointment
```bash
curl -X POST http://localhost:8004/v1/appointments/123/complete \
  -H "X-Correlation-ID: complete-123"
```

### Mark No-Show
```bash
curl -X POST http://localhost:8004/v1/appointments/123/noshow \
  -H "X-Correlation-ID: noshow-123"
```

## Billing Service

### Create Bill
```bash
curl -X POST http://localhost:8003/v1/bills \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": 1,
    "appointment_id": 123,
    "amount": 500.00
  }'
```

### Get Bills
```bash
# All bills
curl http://localhost:8003/v1/bills

# By patient
curl "http://localhost:8003/v1/bills?patient_id=1"

# By status
curl "http://localhost:8003/v1/bills?status=OPEN"
```

### Void Bill
```bash
curl -X POST http://localhost:8003/v1/bills/456/void
```

## Payment Service

### Create Payment (Idempotent)
```bash
curl -X POST http://localhost:8006/v1/payments \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: payment-123-abc" \
  -d '{
    "bill_id": 456,
    "amount": 525.00,
    "method": "UPI"
  }'

# Retry with same key (idempotent - returns same payment)
curl -X POST http://localhost:8006/v1/payments \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: payment-123-abc" \
  -d '{
    "bill_id": 456,
    "amount": 525.00,
    "method": "UPI"
  }'
```

### Get Payments
```bash
curl http://localhost:8006/v1/payments

# By bill
curl "http://localhost:8006/v1/payments?bill_id=456"
```

## Prescription Service

### Create Prescription
```bash
curl -X POST http://localhost:8005/v1/prescriptions \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": 123,
    "patient_id": 1,
    "doctor_id": 1,
    "medication": "Paracetamol",
    "dosage": "0-1-1",
    "days": 5
  }'
```

### Get Prescriptions
```bash
curl http://localhost:8005/v1/prescriptions

# By patient
curl "http://localhost:8005/v1/prescriptions?patient_id=1"

# By appointment
curl "http://localhost:8005/v1/prescriptions?appointment_id=123"
```

## Notification Service

### Send Notification
```bash
curl -X POST http://localhost:8007/v1/notifications \
  -H "Content-Type: application/json" \
  -d '{
    "event_type": "APPOINTMENT_CONFIRMED",
    "channel": "SMS",
    "recipient": "+1234567890",
    "message": "Your appointment is confirmed for Jan 20, 10:00 AM",
    "metadata": {
      "appointment_id": 123,
      "doctor_name": "Dr. Smith"
    }
  }'
```

## Complete Workflow Example

### 1. Create Patient and Doctor (if not exists)
```bash
# Create patient
curl -X POST http://localhost:8001/v1/patients \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jane Doe",
    "email": "jane@example.com",
    "phone": "9876543210",
    "dob": "1985-05-20"
  }'

# Get doctor
curl http://localhost:8002/v1/doctors/1
```

### 2. Book Appointment
```bash
curl -X POST http://localhost:8004/v1/appointments \
  -H "Content-Type: application/json" \
  -H "X-Correlation-ID: workflow-001" \
  -d '{
    "patient_id": 1,
    "doctor_id": 1,
    "department": "Cardiology",
    "slot_start": "2025-01-25T14:00:00",
    "slot_end": "2025-01-25T14:30:00"
  }'
```

### 3. Appointment is Completed → Bill Created Automatically
```bash
curl -X POST http://localhost:8004/v1/appointments/1/complete \
  -H "X-Correlation-ID: workflow-001"

# This triggers bill creation at billing service
```

### 4. Make Payment
```bash
curl -X POST http://localhost:8006/v1/payments \
  -H "Content-Type: application/json" \
  -H "Idempotency-Key: unique-payment-key-001" \
  -d '{
    "bill_id": 1,
    "amount": 525.00,
    "method": "UPI"
  }'
```

### 5. Create Prescription
```bash
curl -X POST http://localhost:8005/v1/prescriptions \
  -H "Content-Type: application/json" \
  -d '{
    "appointment_id": 1,
    "patient_id": 1,
    "doctor_id": 1,
    "medication": "Amoxicillin",
    "dosage": "1-0-1",
    "days": 7
  }'
```

## Error Handling

All services follow a standard error format:

```json
{
  "code": "RESOURCE_NOT_FOUND",
  "message": "Patient not found",
  "correlation_id": "abc-123-xyz"
}
```

Common HTTP status codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Invalid input
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource conflict
- `500 Internal Server Error` - Server error

## Pagination

All list endpoints support pagination:

```bash
# Page 1 (first 20 items)
curl "http://localhost:8001/v1/patients?skip=0&limit=20"

# Page 2 (next 20 items)
curl "http://localhost:8001/v1/patients?skip=20&limit=20"

# Page 3
curl "http://localhost:8001/v1/patients?skip=40&limit=20"
```

## Filtering

Most endpoints support filtering:

```bash
# Filter by name
curl "http://localhost:8001/v1/patients?name=John"

# Filter by department
curl "http://localhost:8002/v1/doctors?department=Cardiology"

# Filter by status
curl "http://localhost:8004/v1/appointments?status=SCHEDULED"
```

## Health Checks

All services expose a health endpoint:

```bash
curl http://localhost:8001/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
curl http://localhost:8006/health
curl http://localhost:8007/health
```

