# Deployment Guide

## Prerequisites

- Docker & Docker Compose
- Kubernetes (Minikube) - optional
- Python 3.11+ - for local development
- PostgreSQL - optional (for production)

## Local Development Setup

### Step 1: Clone and Setup

```bash
# Navigate to project directory
cd Scalable_Assignment

# Install Python dependencies (if running locally)
pip install -r requirements.txt
```

### Step 2: Start with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Step 3: Verify Services

```bash
# Check all services are running
docker-compose ps

# Test health endpoints
curl http://localhost:8001/health  # Patient Service
curl http://localhost:8002/health  # Doctor Service
curl http://localhost:8003/health  # Billing Service
curl http://localhost:8004/health  # Appointment Service
curl http://localhost:8005/health  # Prescription Service
curl http://localhost:8006/health  # Payment Service
curl http://localhost:8007/health  # Notification Service
```

### Step 4: Seed Sample Data

```bash
# Install requests library
pip install requests

# Run seeding script
python scripts/seed_data.py
```

## Kubernetes Deployment (Minikube)

### Step 1: Start Minikube

```bash
# Start Minikube with sufficient resources
minikube start --memory=4096 --cpus=2

# Enable ingress addon
minikube addons enable ingress

# Verify
kubectl get nodes
```

### Step 2: Build and Load Docker Images

```bash
# Build images
docker build -t patient-service:latest ./patient-service
docker build -t doctor-service:latest ./doctor-service
docker build -t appointment-service:latest ./appointment-service
docker build -t billing-service:latest ./billing-service
docker build -t prescription-service:latest ./prescription-service
docker build -t payment-service:latest ./payment-service
docker build -t notification-service:latest ./notification-service

# Load into Minikube
eval $(minikube docker-env)

docker load -i patient-service:latest
docker load -i doctor-service:latest
docker load -i appointment-service:latest
docker load -i billing-service:latest
docker load -i prescription-service:latest
docker load -i payment-service:latest
docker load -i notification-service:latest
```

### Step 3: Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/

# Or apply individually
kubectl apply -f k8s/patient-service-deployment.yaml
kubectl apply -f k8s/doctor-service-deployment.yaml
kubectl apply -f k8s/appointment-service-deployment.yaml
kubectl apply -f k8s/billing-service-deployment.yaml
kubectl apply -f k8s/prescription-service-deployment.yaml
kubectl apply -f k8s/payment-service-deployment.yaml
kubectl apply -f k8s/notification-service-deployment.yaml
kubectl apply -f k8s/ingress.yaml
```

### Step 4: Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check deployments
kubectl get deployments

# Check logs
kubectl logs -f deployment/patient-service
```

### Step 5: Access Services

```bash
# Port forward to access services
kubectl port-forward service/patient-service 8001:8001 &
kubectl port-forward service/doctor-service 8002:8002 &
kubectl port-forward service/appointment-service 8004:8004 &
kubectl port-forward service/billing-service 8003:8003 &

# Or access via ingress
minikube tunnel

# Add to /etc/hosts
# 127.0.0.1 hms.local

# Access via browser
# http://hms.local/v1/patients
```

### Step 6: Cleanup

```bash
# Delete all resources
kubectl delete -f k8s/

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Production Deployment Considerations

### 1. Database
Replace SQLite with PostgreSQL:
```yaml
env:
  - name: DATABASE_URL
    value: "postgresql://user:pass@postgres:5432/patient_db"
```

### 2. Secrets Management
Use Kubernetes Secrets:
```bash
kubectl create secret generic db-secret \
  --from-literal=username=admin \
  --from-literal=password=secret
```

### 3. ConfigMaps
Externalize configuration:
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_URL: "postgresql://..."
```

### 4. Auto-scaling
Enable HPA (Horizontal Pod Autoscaler):
```bash
kubectl autoscale deployment appointment-service \
  --cpu-percent=70 \
  --min=2 --max=10
```

### 5. Monitoring
Integrate with Prometheus and Grafana for full observability.

## Testing

### Unit Tests
```bash
cd patient-service
pytest
```

### Integration Tests
```bash
# Test API endpoints
curl http://localhost:8001/v1/patients | jq .
curl http://localhost:8002/v1/doctors | jq .
curl http://localhost:8004/v1/appointments | jq .
```

### Load Testing
```bash
# Use Apache Bench or k6
ab -n 1000 -c 10 http://localhost:8004/v1/appointments
```

## Troubleshooting

### Services not starting
```bash
# Check Docker logs
docker-compose logs -f

# Restart services
docker-compose restart
```

### Database issues
```bash
# Reset databases
docker-compose down -v
docker-compose up
```

### Port conflicts
```bash
# Change ports in docker-compose.yml
ports:
  - "8005:8001"  # Change host port
```

### Kubernetes pods crashing
```bash
# Check logs
kubectl logs -f deployment/patient-service

# Describe pod
kubectl describe pod <pod-name>

# Check events
kubectl get events
```

## Performance Optimization

1. **Connection Pooling**: Configure SQLAlchemy pool size
2. **Caching**: Add Redis for frequently accessed data
3. **CDN**: Use CDN for static assets
4. **Database Indexing**: Add indexes on frequently queried fields
5. **Async Operations**: Use Celery for background jobs

## Security Checklist

- [ ] Enable HTTPS with TLS certificates
- [ ] Use secrets management (Vault, AWS Secrets Manager)
- [ ] Implement rate limiting
- [ ] Add authentication/authorization (JWT)
- [ ] Enable audit logging
- [ ] Regular security scans
- [ ] Backup databases regularly
- [ ] Encrypt sensitive data at rest

