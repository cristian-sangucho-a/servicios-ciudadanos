"""
Gestor de usuarios para el modelo Ciudadano.
"""
from django.contrib.auth.models import BaseUserManager


class GestorCiudadano(BaseUserManager):
    """
    Gestor personalizado para el modelo Ciudadano.
    """

    def create_user(self, correo_electronico, nombre_completo, numero_identificacion, contrasena=None):
        """
        Crea y guarda un usuario regular.
        """
        if not correo_electronico:
            raise ValueError('Los usuarios deben tener un correo electrónico')

        user = self.model(
            correo_electronico=self.normalize_email(correo_electronico),
            nombre_completo=nombre_completo,
            numero_identificacion=numero_identificacion,
        )

        user.set_password(contrasena)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, nombre_completo, numero_identificacion, contrasena=None):
        """
        Crea y guarda un superusuario.
        """
        user = self.create_user(
            correo_electronico=correo_electronico,
            contrasena=contrasena,
            nombre_completo=nombre_completo,
            numero_identificacion=numero_identificacion,
        )

        user.is_staff = True
        user.is_superuser = True
        user.esta_activo = True  # Asegurarnos de que el usuario esté activo
        user.save(using=self._db)
        return user
