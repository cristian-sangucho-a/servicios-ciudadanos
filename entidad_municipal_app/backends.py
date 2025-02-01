from django.contrib.auth.backends import BaseBackend
from .models import EntidadMunicipal

class EntidadBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # El correo puede venir como username o como correo_electronico
            correo = username or kwargs.get('correo_electronico')
            if not correo:
                return None
            
            entidad = EntidadMunicipal.objects.get(correo_electronico=correo)
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
