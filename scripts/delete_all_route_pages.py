import os
import sys
import django
import requests
import json

# Step 1: Setup Django
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "skycms.settings.dev")
django.setup()

from routes.models import RoutePage

count = RoutePage.objects.all().delete()
print(f"✅ Deleted {count} RoutePage(s).")
