from django.contrib.auth.backends import BaseBackend
from .models import EntidadMunicipal

class EntidadBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            entidad = EntidadMunicipal.objects.get(correo_electronico=username)
            if entidad.check_password(password):
                return entidad
        except EntidadMunicipal.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return EntidadMunicipal.objects.get(pk=user_id)
        except EntidadMunicipal.DoesNotExist:
            return None
