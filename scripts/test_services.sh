#!/bin/bash

# Test all microservices
echo "Testing HMS Microservices..."

# Test Patient Service
echo "Testing Patient Service..."
curl -s http://localhost:8001/health | jq .

# Test Doctor Service
echo "Testing Doctor Service..."
curl -s http://localhost:8002/health | jq .

# Test Appointment Service
echo "Testing Appointment Service..."
curl -s http://localhost:8004/health | jq .

# Test Billing Service
echo "Testing Billing Service..."
curl -s http://localhost:8003/health | jq .

# Test Prescription Service
echo "Testing Prescription Service..."
curl -s http://localhost:8005/health | jq .

# Test Payment Service
echo "Testing Payment Service..."
curl -s http://localhost:8006/health | jq .

# Test Notification Service
echo "Testing Notification Service..."
curl -s http://localhost:8007/health | jq .

echo "All services tested!"

