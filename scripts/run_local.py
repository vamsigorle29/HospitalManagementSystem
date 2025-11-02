"""
Script to run all microservices locally
"""
import subprocess
import sys
import os
import time
import signal
from pathlib import Path

# Get the project root directory (parent of scripts/)
PROJECT_ROOT = Path(__file__).parent.parent

# Service configurations
SERVICES = {
    "patient-service": {
        "port": 8001,
        "path": PROJECT_ROOT / "patient-service",
        "env": {
            "PORT": "8001",
            "DATABASE_URL": f"sqlite:///./patient.db",
        }
    },
    "doctor-service": {
        "port": 8002,
        "path": PROJECT_ROOT / "doctor-service",
        "env": {
            "PORT": "8002",
            "DATABASE_URL": f"sqlite:///./doctor.db",
        }
    },
    "billing-service": {
        "port": 8003,
        "path": PROJECT_ROOT / "billing-service",
        "env": {
            "PORT": "8003",
            "DATABASE_URL": f"sqlite:///./billing.db",
        }
    },
    "appointment-service": {
        "port": 8004,
        "path": PROJECT_ROOT / "appointment-service",
        "env": {
            "PORT": "8004",
            "DATABASE_URL": f"sqlite:///./appointment.db",
            "PATIENT_SERVICE_URL": "http://localhost:8001",
            "DOCTOR_SERVICE_URL": "http://localhost:8002",
            "BILLING_SERVICE_URL": "http://localhost:8003",
            "NOTIFICATION_SERVICE_URL": "http://localhost:8007",
        }
    },
    "prescription-service": {
        "port": 8005,
        "path": PROJECT_ROOT / "prescription-service",
        "env": {
            "PORT": "8005",
            "DATABASE_URL": f"sqlite:///./prescription.db",
        }
    },
    "payment-service": {
        "port": 8006,
        "path": PROJECT_ROOT / "payment-service",
        "env": {
            "PORT": "8006",
            "DATABASE_URL": f"sqlite:///./payment.db",
        }
    },
    "notification-service": {
        "port": 8007,
        "path": PROJECT_ROOT / "notification-service",
        "env": {
            "PORT": "8007",
            "DATABASE_URL": f"sqlite:///./notification.db",
        }
    },
}

processes = []

def signal_handler(sig, frame):
    """Handle Ctrl+C to gracefully stop all services"""
    print("\n\nStopping all services...")
    for process in processes:
        try:
            process.terminate()
        except:
            pass
    time.sleep(1)
    for process in processes:
        try:
            process.kill()
        except:
            pass
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

def start_service(name, config):
    """Start a single service"""
    print(f"\n{'='*60}")
    print(f"Starting {name} on port {config['port']}...")
    print(f"{'='*60}")
    
    env = os.environ.copy()
    env.update(config["env"])
    
    try:
        # Change to service directory
        os.chdir(config["path"])
        
        # Start the service
        process = subprocess.Popen(
            [sys.executable, "app.py"],
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        processes.append(process)
        
        # Print initial output
        if process.stdout:
            print(f"[{name}] Process started with PID {process.pid}")
        
        return process
    except Exception as e:
        print(f"Error starting {name}: {e}")
        return None

def main():
    """Main function to start all services"""
    print("\n" + "="*60)
    print("Hospital Management System - Local Development Mode")
    print("="*60)
    print("\nStarting all microservices...")
    print("Press Ctrl+C to stop all services\n")
    
    # Start all services
    for name, config in SERVICES.items():
        process = start_service(name, config)
        if process:
            time.sleep(1)  # Small delay between service starts
    
    print("\n" + "="*60)
    print("All services started!")
    print("="*60)
    print("\nService URLs:")
    for name, config in SERVICES.items():
        print(f"  {name:20s}: http://localhost:{config['port']}/docs")
    print("\nHealth Check URLs:")
    for name, config in SERVICES.items():
        print(f"  {name:20s}: http://localhost:{config['port']}/health")
    print("\nPress Ctrl+C to stop all services\n")
    
    # Wait for all processes
    try:
        for process in processes:
            process.wait()
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == "__main__":
    main()

