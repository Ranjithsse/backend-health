import requests
import json

base_url = "http://10.187.32.85:8000"

print(f"Testing connectivity to {base_url}...")
try:
    r = requests.get(f"{base_url}/api/config/")
    print(f"Config GET: {r.status_code}")
    print(f"Response: {r.text[:100]}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting Signup (POST)...")
signup_data = {
    "username": "testuser_unique_123",
    "email": "testuser_unique_123@example.com",
    "password": "testpassword123",
    "hospital_name": "Test Hospital",
    "specialization": "General"
}
try:
    r = requests.post(f"{base_url}/api/signup/", json=signup_data)
    print(f"Signup POST: {r.status_code}")
    print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting Login (POST)...")
login_data = {
    "username": "ranjithkumar8032@gmail.com",
    "password": "wrongpassword"
}
try:
    r = requests.post(f"{base_url}/api/login/", json=login_data)
    print(f"Login POST: {r.status_code}")
    print(f"Response: {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")
