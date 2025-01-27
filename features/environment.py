import os
import django

def before_all(context):
    # Point to your Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servicios_ciudadanos.settings")
    # Initialize Django
    django.setup()
