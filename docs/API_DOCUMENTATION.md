# API Documentation - Hospital Management System

This document provides comprehensive API documentation for all microservices in the Hospital Management System.

## OpenAPI/Swagger Documentation

All services provide interactive API documentation via Swagger UI and ReDoc:

### Service Documentation URLs

| Service | Swagger UI | ReDoc | OpenAPI JSON |
|---------|-----------|-------|--------------|
| Patient Service | http://localhost:8001/v1/docs | http://localhost:8001/v1/redoc | http://localhost:8001/v1/openapi.json |
| Doctor Service | http://localhost:8002/v1/docs | http://localhost:8002/v1/redoc | http://localhost:8002/v1/openapi.json |
| Billing Service | http://localhost:8003/v1/docs | http://localhost:8003/v1/redoc | http://localhost:8003/v1/openapi.json |
| Appointment Service | http://localhost:8004/v1/docs | http://localhost:8004/v1/redoc | http://localhost:8004/v1/openapi.json |
| Prescription Service | http://localhost:8005/v1/docs | http://localhost:8005/v1/redoc | http://localhost:8005/v1/openapi.json |
| Payment Service | http://localhost:8006/v1/docs | http://localhost:8006/v1/redoc | http://localhost:8006/v1/openapi.json |
| Notification Service | http://localhost:8007/v1/docs | http://localhost:8007/v1/redoc | http://localhost:8007/v1/openapi.json |

## API Versioning

All services use `/v1` prefix for API versioning:
- All endpoints are under `/v1/` path
- OpenAPI documentation is at `/v1/docs` and `/v1/redoc`
- OpenAPI JSON schema is at `/v1/openapi.json`

## Common Headers

### Correlation ID
All services support `X-Correlation-ID` header for request tracing:
```
X-Correlation-ID: <unique-id>
```

### Idempotency Key
Services that support idempotent operations use `Idempotency-Key` header:
```
Idempotency-Key: <unique-key>
```

## Service-Specific Documentation

### 1. Patient Service (Port 8001)

**Base URL:** `http://localhost:8001/v1`

**Endpoints:**
- `POST /v1/patients` - Create patient
- `GET /v1/patients/{patient_id}` - Get patient by ID
- `GET /v1/patients` - List patients (with pagination)
- `PUT /v1/patients/{patient_id}` - Update patient
- `GET /v1/patients/{patient_id}/exists` - Check if patient exists
- `GET /health` - Health check

**Features:**
- PII masking in logs
- Pagination support
- Filtering support

**Swagger:** http://localhost:8001/v1/docs

### 2. Doctor Service (Port 8002)

**Base URL:** `http://localhost:8002/v1`

**Endpoints:**
- `POST /v1/doctors` - Create doctor
- `GET /v1/doctors/{doctor_id}` - Get doctor by ID
- `GET /v1/doctors` - List doctors (with filtering)
- `GET /v1/doctors/{doctor_id}/availability` - Check availability
- `GET /v1/doctors/{doctor_id}/department` - Get doctor's department
- `GET /health` - Health check

**Features:**
- Department and specialization filtering
- Availability checking
- Clinic hours: 9 AM - 6 PM

**Swagger:** http://localhost:8002/v1/docs

### 3. Billing Service (Port 8003)

**Base URL:** `http://localhost:8003/v1`

**Endpoints:**
- `POST /v1/bills` - Create bill (with 5% tax)
- `GET /v1/bills/{bill_id}` - Get bill by ID
- `GET /v1/bills` - List bills (with filtering)
- `GET /health` - Health check

**Features:**
- Automatic 5% tax calculation
- Integration with appointment service
- Correlation ID support

**Swagger:** http://localhost:8003/v1/docs

### 4. Appointment Service (Port 8004)

**Base URL:** `http://localhost:8004/v1`

**Endpoints:**
- `POST /v1/appointments` - Book appointment (idempotent)
- `GET /v1/appointments/{appointment_id}` - Get appointment by ID
- `GET /v1/appointments` - List appointments (with filtering)
- `POST /v1/appointments/{appointment_id}/reschedule` - Reschedule appointment
- `POST /v1/appointments/{appointment_id}/cancel` - Cancel appointment
- `POST /v1/appointments/{appointment_id}/complete` - Complete appointment
- `POST /v1/appointments/{appointment_id}/noshow` - Mark as no-show
- `GET /health` - Health check

**Features:**
- Idempotency support via `Idempotency-Key` header
- Correlation ID support
- Business rules validation:
  - Minimum 2-hour lead time
  - Clinic hours: 9 AM - 6 PM
  - Maximum 2 reschedules
  - Maximum 8 appointments/day per doctor
- Automatic bill creation on completion

**Swagger:** http://localhost:8004/v1/docs

### 5. Prescription Service (Port 8005)

**Base URL:** `http://localhost:8005/v1`

**Endpoints:**
- `POST /v1/prescriptions` - Create prescription
- `GET /v1/prescriptions/{prescription_id}` - Get prescription by ID
- `GET /v1/prescriptions` - List prescriptions (with filtering)
- `GET /health` - Health check

**Features:**
- Appointment validation (must be COMPLETED)
- Automatic notification trigger
- Correlation ID support
- Patient and doctor validation

**Swagger:** http://localhost:8005/v1/docs

### 6. Payment Service (Port 8006)

**Base URL:** `http://localhost:8006/v1`

**Endpoints:**
- `POST /v1/payments` - Create payment (idempotent)
- `GET /v1/payments/{payment_id}` - Get payment by ID
- `GET /v1/payments` - List payments (with filtering)
- `GET /health` - Health check

**Features:**
- Idempotency support via `Idempotency-Key` header
- No double-charging on retries
- Bill integration

**Swagger:** http://localhost:8006/v1/docs

### 7. Notification Service (Port 8007)

**Base URL:** `http://localhost:8007/v1`

**Endpoints:**
- `POST /v1/notifications` - Send notification
- `GET /v1/notifications` - List notifications
- `GET /health` - Health check

**Features:**
- Event-driven notifications
- SMS/Email support (simulated)
- Integration with all services

**Swagger:** http://localhost:8007/v1/docs

## OpenAPI Specification

Each service exposes its OpenAPI 3.0 specification at `/v1/openapi.json`. This can be used to:

1. **Generate client SDKs** using tools like:
   - `openapi-generator`
   - `swagger-codegen`
   - Language-specific generators

2. **Import into API testing tools** like:
   - Postman
   - Insomnia
   - REST Client

3. **Generate documentation** using:
   - Swagger UI (already available at `/v1/docs`)
   - ReDoc (already available at `/v1/redoc`)
   - Custom documentation generators

## Example: Generating Client SDK

```bash
# Install OpenAPI Generator
npm install -g @openapitools/openapi-generator-cli

# Generate Python client for Patient Service
openapi-generator-cli generate \
  -i http://localhost:8001/v1/openapi.json \
  -g python \
  -o ./generated-clients/patient-service-python

# Generate TypeScript client for Appointment Service
openapi-generator-cli generate \
  -i http://localhost:8004/v1/openapi.json \
  -g typescript-axios \
  -o ./generated-clients/appointment-service-typescript
```

## Example: Importing into Postman

1. Open Postman
2. Click "Import"
3. Select "Link" tab
4. Enter: `http://localhost:8001/v1/openapi.json`
5. Click "Continue" and "Import"

## API Testing

All services can be tested directly from Swagger UI:

1. Navigate to service's Swagger UI (e.g., http://localhost:8001/v1/docs)
2. Click "Try it out" on any endpoint
3. Fill in required parameters
4. Click "Execute"
5. View response

## Common Response Formats

### Success Response
```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

### Error Response
```json
{
  "detail": "Error message",
  "correlation_id": "uuid-here"
}
```

### Paginated Response
```json
[
  {
    "id": 1,
    "field1": "value1"
  },
  {
    "id": 2,
    "field1": "value2"
  }
]
```

## Health Checks

All services provide health check endpoints:
- `GET /health` - Returns service health status

Example response:
```json
{
  "status": "healthy",
  "service": "patient-service"
}
```

## Accessing Documentation

### When Services Are Running Locally

1. Start all services:
   ```bash
   python scripts/run_local.py
   ```

2. Open browser and navigate to any service's Swagger UI:
   - Patient: http://localhost:8001/v1/docs
   - Doctor: http://localhost:8002/v1/docs
   - etc.

### When Services Are Running in Docker

1. Start services:
   ```bash
   docker-compose up
   ```

2. Access Swagger UI using the same URLs (ports are mapped)

### When Services Are Running in Kubernetes

1. Port forward to access services:
   ```bash
   kubectl port-forward service/patient-service 8001:8001
   ```

2. Access Swagger UI at http://localhost:8001/v1/docs

## OpenAPI Schema Details

Each service's OpenAPI schema includes:

- **Info**: Title, version, description
- **Servers**: Base URLs and environments
- **Paths**: All available endpoints
- **Components**: Request/response schemas
- **Security**: Authentication schemes (if applicable)
- **Tags**: Endpoint grouping

## Exporting OpenAPI Schemas

To save OpenAPI schemas to files:

```bash
# Save all service schemas
curl http://localhost:8001/v1/openapi.json -o patient-service-openapi.json
curl http://localhost:8002/v1/openapi.json -o doctor-service-openapi.json
curl http://localhost:8003/v1/openapi.json -o billing-service-openapi.json
curl http://localhost:8004/v1/openapi.json -o appointment-service-openapi.json
curl http://localhost:8005/v1/openapi.json -o prescription-service-openapi.json
curl http://localhost:8006/v1/openapi.json -o payment-service-openapi.json
curl http://localhost:8007/v1/openapi.json -o notification-service-openapi.json
```

## Integration with API Gateways

The OpenAPI specifications can be imported into API gateways like:
- Kong
- AWS API Gateway
- Azure API Management
- Google Cloud Endpoints

This enables:
- Rate limiting
- Authentication/Authorization
- Request/Response transformation
- Analytics and monitoring

## Summary

All services are fully documented with OpenAPI 3.0 specifications accessible via:
- **Interactive Swagger UI**: `/v1/docs`
- **ReDoc Documentation**: `/v1/redoc`
- **OpenAPI JSON Schema**: `/v1/openapi.json`

The documentation is automatically generated from the FastAPI application code and stays in sync with the implementation.

