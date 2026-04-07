import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from user.models import CustomUser

email = 'ranjithkumar8032@gmail.com'
try:
    user = CustomUser.objects.get(email=email)
    print(f"User found: {user.username}, email: {user.email}")
except CustomUser.DoesNotExist:
    print(f"User with email {email} not found.")

# List all users
print("\nAll users:")
for u in CustomUser.objects.all():
    print(f"- {u.username} ({u.email})")
