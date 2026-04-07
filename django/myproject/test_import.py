import os
import django
from django.conf import settings

try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    django.setup()
    print("Django setup successful")
except Exception as e:
    import traceback
    traceback.print_exc()
