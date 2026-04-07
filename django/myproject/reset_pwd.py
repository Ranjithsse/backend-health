import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()
from user.models import CustomUser

email = 'ranjithkumar8032@gmail.com'
try:
    user = CustomUser.objects.get(email=email)
    user.set_password('password123')
    user.save()
    print(f"Password reset successful for {email}. New password: password123")
except CustomUser.DoesNotExist:
    print(f"User {email} not found.")

# Also check for 'ranjithkumar' username
try:
    user = CustomUser.objects.get(username='ranjithkumar')
    user.set_password('password123')
    user.save()
    print(f"Password reset successful for username 'ranjithkumar'. New password: password123")
except CustomUser.DoesNotExist:
    pass
