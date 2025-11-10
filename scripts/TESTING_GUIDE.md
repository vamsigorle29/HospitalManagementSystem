# Testing Guide - Running Tests After Cloning All Repositories

This guide explains how to set up and test all microservices when they are in separate GitHub repositories.

## Prerequisites

- Python 3.8+ installed
- Git installed
- All 7 service repositories cloned

## Repository Structure

After cloning all repositories, you should have this structure:

```
your-workspace/
├── patient-service/          (from https://github.com/vamsigorle29/patient-service)
├── doctor-service/           (from https://github.com/vamsigorle29/doctor-service)
├── billing-service/          (from https://github.com/vamsigorle29/billing-service)
├── appointment-service/      (from https://github.com/vamsigorle29/appointment-service)
├── prescription-service/     (from https://github.com/vamsigorle29/prescription-service)
├── payment-service/          (from https://github.com/vamsigorle29/payment-service)
└── notification-service/     (from https://github.com/vamsigorle29/notification-service)
```

## Step 1: Clone All Repositories

Clone all 7 service repositories:

```bash
# Create a workspace directory
mkdir hms-workspace
cd hms-workspace

# Clone all repositories
git clone https://github.com/vamsigorle29/patient-service.git
git clone https://github.com/vamsigorle29/doctor-service.git
git clone https://github.com/vamsigorle29/billing-service.git
git clone https://github.com/vamsigorle29/appointment-service.git
git clone https://github.com/vamsigorle29/prescription-service.git
git clone https://github.com/vamsigorle29/payment-service.git
git clone https://github.com/vamsigorle29/notification-service.git
```

## Step 2: Install Dependencies

Install Python dependencies for each service:

```bash
# Patient Service
cd patient-service
pip install -r requirements.txt
cd ..

# Doctor Service
cd doctor-service
pip install -r requirements.txt
cd ..

# Billing Service
cd billing-service
pip install -r requirements.txt
cd ..

# Appointment Service
cd appointment-service
pip install -r requirements.txt
cd ..

# Prescription Service
cd prescription-service
pip install -r requirements.txt
cd ..

# Payment Service
cd payment-service
pip install -r requirements.txt
cd ..

# Notification Service
cd notification-service
pip install -r requirements.txt
cd ..
```

### Quick Install Script (PowerShell)

```powershell
$services = @(
    "patient-service",
    "doctor-service",
    "billing-service",
    "appointment-service",
    "prescription-service",
    "payment-service",
    "notification-service"
)

foreach ($service in $services) {
    Write-Host "Installing dependencies for $service..." -ForegroundColor Yellow
    cd $service
    pip install -r requirements.txt
    cd ..
    Write-Host "✓ $service dependencies installed`n" -ForegroundColor Green
}
```

## Step 3: Start All Services

You have two options to start all services:

### Option A: Using run_local.py (Recommended)

If you have the original monorepo with `scripts/run_local.py`, you can use it:

```bash
# From the original HospitalManagementSystem directory
python scripts/run_local.py
```

This will start all 7 services automatically.

### Option B: Manual Start (Separate Terminals)

Start each service in a separate terminal:

**Terminal 1 - Patient Service:**
```bash
cd patient-service
python app.py
```

**Terminal 2 - Doctor Service:**
```bash
cd doctor-service
python app.py
```

**Terminal 3 - Billing Service:**
```bash
cd billing-service
python app.py
```

**Terminal 4 - Appointment Service:**
```bash
cd appointment-service
python app.py
```

**Terminal 5 - Prescription Service:**
```bash
cd prescription-service
python app.py
```

**Terminal 6 - Payment Service:**
```bash
cd payment-service
python app.py
```

**Terminal 7 - Notification Service:**
```bash
cd notification-service
python app.py
```

### Option C: Using Docker Compose (If Available)

If you have a docker-compose.yml that references all services:

```bash
docker-compose up
```

## Step 4: Verify Services Are Running

Check that all services are healthy:

```bash
# Check each service
curl http://localhost:8001/health  # Patient Service
curl http://localhost:8002/health  # Doctor Service
curl http://localhost:8003/health  # Billing Service
curl http://localhost:8004/health  # Appointment Service
curl http://localhost:8005/health  # Prescription Service
curl http://localhost:8006/health  # Payment Service
curl http://localhost:8007/health  # Notification Service
```

Or use PowerShell:

```powershell
$ports = @(8001, 8002, 8003, 8004, 8005, 8006, 8007)
$services = @("patient", "doctor", "billing", "appointment", "prescription", "payment", "notification")

for ($i = 0; $i -lt $ports.Length; $i++) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$($ports[$i])/health" -TimeoutSec 2 -UseBasicParsing
        Write-Host "[OK] $($services[$i])-service (port $($ports[$i]))" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] $($services[$i])-service (port $($ports[$i]))" -ForegroundColor Red
    }
}
```

## Step 5: Run Tests

Once all services are running, execute the test script:

```bash
# From the original HospitalManagementSystem directory (if you have it)
python scripts/test_local.py
```

### If You Don't Have the Original Scripts

If you only have the separate repositories, you can:

1. **Clone the original repository** to get the test scripts:
   ```bash
   git clone <original-repo-url> HospitalManagementSystem
   cd HospitalManagementSystem
   python scripts/test_local.py
   ```

2. **Or create a simple test script** in your workspace:

```python
# test_all_services.py
import requests
import time

SERVICES = {
    "patient": "http://localhost:8001",
    "doctor": "http://localhost:8002",
    "billing": "http://localhost:8003",
    "appointment": "http://localhost:8004",
    "prescription": "http://localhost:8005",
    "payment": "http://localhost:8006",
    "notification": "http://localhost:8007"
}

print("Testing all services...")
for name, url in SERVICES.items():
    try:
        response = requests.get(f"{url}/health", timeout=2)
        if response.status_code == 200:
            print(f"✓ {name}-service: {response.json()}")
        else:
            print(f"✗ {name}-service: Status {response.status_code}")
    except Exception as e:
        print(f"✗ {name}-service: {e}")
```

## Test Cases Covered

The test script (`test_local.py`) covers:

### 1. Patient Service Tests
- Create Patient
- Get Patient by ID
- List Patients (with pagination)
- Update Patient
- Check Patient Exists

### 2. Doctor Service Tests
- Create Doctor
- Get Doctor by ID
- List Doctors (with filtering)
- Check Doctor Availability
- Get Doctor Department

### 3. Appointment Service Tests
- Create Appointment (with business rules validation)
- Get Appointment by ID
- List Appointments
- Complete Appointment (triggers bill creation)

### 4. Billing Service Tests
- Create Bill (with 5% tax calculation)
- Get Bill by ID
- List Bills

### 5. Payment Service Tests
- Create Payment (with idempotency)
- Test Payment Idempotency (same key returns same payment)
- Get Payment by ID
- List Payments

### 6. Prescription Service Tests
- Create Prescription
- Get Prescription by ID
- List Prescriptions

### 7. Notification Service Tests
- Send Notification
- List Notifications

## Expected Test Results

When all services are running correctly, you should see:

```
Total Tests: 26
Passed: 26
Failed: 0
Success Rate: 100.0%

[SUCCESS] All API tests passed!
```

## Troubleshooting

### Services Not Starting

**Issue:** Service fails to start
- Check if port is already in use: `netstat -ano | findstr :8001`
- Verify dependencies are installed: `pip list | findstr fastapi`
- Check for errors in the service logs

**Solution:**
```bash
# Kill process on port (Windows)
netstat -ano | findstr :8001
taskkill /PID <PID> /F
```

### Connection Timeouts

**Issue:** Tests timeout when connecting to services
- Services may not be fully started yet
- Wait 10-15 seconds after starting services
- Check firewall settings

**Solution:**
```bash
# Wait longer before running tests
# Or increase timeout in test script
```

### Import Errors

**Issue:** `ModuleNotFoundError` when starting services
- Dependencies not installed
- Wrong Python environment

**Solution:**
```bash
# Install dependencies
pip install -r requirements.txt

# Or use virtual environment
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Appointment Creation Fails

**Issue:** "Appointments must be between 9 AM and 6 PM"
- Test is trying to create appointment outside clinic hours
- Fixed in latest version of test script

**Solution:** Use the updated `test_local.py` script

## Environment Variables

Some services may need environment variables set:

### Appointment Service
```bash
export PATIENT_SERVICE_URL=http://localhost:8001
export DOCTOR_SERVICE_URL=http://localhost:8002
export BILLING_SERVICE_URL=http://localhost:8003
export NOTIFICATION_SERVICE_URL=http://localhost:8007
```

Or in PowerShell:
```powershell
$env:PATIENT_SERVICE_URL="http://localhost:8001"
$env:DOCTOR_SERVICE_URL="http://localhost:8002"
$env:BILLING_SERVICE_URL="http://localhost:8003"
$env:NOTIFICATION_SERVICE_URL="http://localhost:8007"
```

## Quick Start Script

Create a `start-all.ps1` script in your workspace:

```powershell
# start-all.ps1
$services = @(
    @{Name="patient"; Port=8001; Path="patient-service"},
    @{Name="doctor"; Port=8002; Path="doctor-service"},
    @{Name="billing"; Port=8003; Path="billing-service"},
    @{Name="appointment"; Port=8004; Path="appointment-service"},
    @{Name="prescription"; Port=8005; Path="prescription-service"},
    @{Name="payment"; Port=8006; Path="payment-service"},
    @{Name="notification"; Port=8007; Path="notification-service"}
)

Write-Host "Starting all services..." -ForegroundColor Cyan
foreach ($svc in $services) {
    Write-Host "Starting $($svc.Name)-service on port $($svc.Port)..." -ForegroundColor Yellow
    Start-Process python -ArgumentList "$($svc.Path)\app.py" -WindowStyle Normal
    Start-Sleep -Seconds 2
}

Write-Host "`nAll services started! Wait 10 seconds, then run tests." -ForegroundColor Green
```

## Next Steps

After successful testing:

1. **Deploy to Production**: Each service can be deployed independently
2. **Set up CI/CD**: Create pipelines for each repository
3. **Monitor Services**: Set up logging and monitoring
4. **Scale Services**: Scale individual services based on load

## Additional Resources

- API Documentation: Visit `http://localhost:PORT/docs` for each service
- Service READMEs: Check individual service README.md files
- Docker Deployment: See Dockerfile in each service
- Kubernetes: See k8s/deployment.yaml in each service

