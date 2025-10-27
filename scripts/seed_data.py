"""
Seed data script to load CSV data into microservices
"""
import csv
import requests
from datetime import datetime
import time

BASE_URLS = {
    'patient': 'http://localhost:8001',
    'doctor': 'http://localhost:8002',
    'billing': 'http://localhost:8003',
    'appointment': 'http://localhost:8004',
    'prescription': 'http://localhost:8005',
    'payment': 'http://localhost:8006'
}

def load_patients():
    """Load patients from CSV"""
    print("Loading patients...")
    with open('../hms_patients.csv', 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            try:
                data = {
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'dob': row['dob']
                }
                response = requests.post(f"{BASE_URLS['patient']}/v1/patients", json=data)
                if response.status_code in [200, 201]:
                    count += 1
            except Exception as e:
                print(f"Error loading patient: {e}")
    print(f"Loaded {count} patients")

def load_doctors():
    """Load doctors from CSV"""
    print("Loading doctors...")
    with open('../hms_doctors.csv', 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            try:
                data = {
                    'name': row['name'],
                    'email': row['email'],
                    'phone': row['phone'],
                    'department': row['department'],
                    'specialization': row['specialization']
                }
                response = requests.post(f"{BASE_URLS['doctor']}/v1/doctors", json=data)
                if response.status_code in [200, 201]:
                    count += 1
            except Exception as e:
                print(f"Error loading doctor: {e}")
    print(f"Loaded {count} doctors")

def load_appointments():
    """Load appointments from CSV"""
    print("Loading appointments...")
    with open('../hms_appointments.csv', 'r') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            try:
                # Parse dates
                slot_start = datetime.strptime(row['slot_start'], '%Y-%m-%d %H:%M:%S')
                slot_end = datetime.strptime(row['slot_end'], '%Y-%m-%d %H:%M:%S')
                
                data = {
                    'patient_id': int(row['patient_id']),
                    'doctor_id': int(row['doctor_id']),
                    'department': row['department'],
                    'slot_start': slot_start.isoformat(),
                    'slot_end': slot_end.isoformat(),
                    'status': row['status']
                }
                
                # Try to create appointment
                response = requests.post(f"{BASE_URLS['appointment']}/v1/appointments", json=data)
                if response.status_code in [200, 201]:
                    count += 1
            except Exception as e:
                print(f"Error loading appointment: {e}")
    print(f"Loaded {count} appointments")

def main():
    """Main seeding function"""
    print("Starting data seeding...")
    
    # Wait for services to be ready
    print("Waiting for services to be ready...")
    time.sleep(5)
    
    try:
        load_patients()
        load_doctors()
        load_appointments()
        
        print("\nData seeding complete!")
    except Exception as e:
        print(f"Error during seeding: {e}")

if __name__ == "__main__":
    main()

