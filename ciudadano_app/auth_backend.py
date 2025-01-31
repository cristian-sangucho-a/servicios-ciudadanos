from django.contrib.auth.backends import BaseBackend
from .models import Ciudadano

class CiudadanoBackend(BaseBackend):
    def authenticate(self, request, correo_electronico=None, password=None):
        try:
            user = Ciudadano.objects.get(correo_electronico=correo_electronico)
            if user.check_password(password):
                return user
        except Ciudadano.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Ciudadano.objects.get(pk=user_id)
        except Ciudadano.DoesNotExist:
            return None