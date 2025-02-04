from django.contrib.auth.backends import BaseBackend
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

class CiudadanoBackend(BaseBackend):
    """
    Backend de autenticación para Ciudadano.
    Se basa en el campo 'correo_electronico' y la contraseña.
    """
    def authenticate(self, request, correo_electronico=None, password=None, **kwargs):
        try:
            ciudadano = Ciudadano.objects.get(correo_electronico=correo_electronico)
            if ciudadano.check_password(password):
                return ciudadano
        except Ciudadano.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Ciudadano.objects.get(pk=user_id)
        except Ciudadano.DoesNotExist:
            return None
