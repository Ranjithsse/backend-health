import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from user.models import CustomUser

def fix_user_details():
    email = "ranjithkumar8032@gmail.com"
    try:
        user = CustomUser.objects.get(email=email)
        user.first_name = "Ranjith"
        user.last_name = "Kumar"
        # Since specialization and hospital might be missing for existing users
        if not user.specialization:
            user.specialization = "Internal Medicine"
        if not user.hospital_name:
            user.hospital_name = "City Medical Center"
        user.save()
        print(f"Successfully updated details for {email}")
    except CustomUser.DoesNotExist:
        print(f"User {email} not found")

if __name__ == "__main__":
    fix_user_details()
