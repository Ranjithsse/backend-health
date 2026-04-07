import urllib.request
import json

url = "http://127.0.0.1:8000/api/signup/"
data = {
    "username": "testuser_3",
    "email": "test3@example.com",
    "password": "testpass123",
    "hospital_name": "Test Hospital",
    "specialization": "Testing"
}

req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})

try:
    with urllib.request.urlopen(req) as response:
        print(f"Status: {response.getcode()}")
        print(f"Response: {response.read().decode('utf-8')}")
except urllib.error.HTTPError as e:
    print(f"HTTP Error: {e.code}")
    print(f"Response: {e.read().decode('utf-8')}")
except Exception as e:
    print(f"Error: {e}")
