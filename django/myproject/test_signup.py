import requests
import json

url = "http://127.0.0.1:8000/api/signup/"
data = {
    "username": "testuser_2",
    "email": "test2@example.com",
    "password": "testpass123",
    "hospital_name": "Test Hospital",
    "specialization": "Testing"
}

try:
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
