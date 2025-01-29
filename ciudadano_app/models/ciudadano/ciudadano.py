"""
Modelo principal de Ciudadano.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from ciudadano_app.models.ciudadano.gestor_ciudadano import GestorCiudadano


class Ciudadano(AbstractBaseUser, PermissionsMixin):
    """
    Modelo que representa a un ciudadano en el sistema municipal.
    Extiende el modelo base de usuario de Django para incluir campos específicos.
    """

    correo_electronico = models.EmailField(
        unique=True,
        verbose_name="Correo Electrónico",
        help_text="Dirección de correo electrónico del ciudadano",
    )

    nombre_completo = models.CharField(
        max_length=120,
        verbose_name="Nombre Completo",
        help_text="Nombre completo del ciudadano",
    )

    numero_identificacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Identificación",
        help_text="Número de documento de identidad del ciudadano",
    )

    esta_activo = models.BooleanField(
        default=True,
        verbose_name="¿Está Activo?",
        help_text="Indica si el ciudadano puede acceder al sistema",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="¿Es Personal Administrativo?",
        help_text="Indica si el ciudadano puede acceder al panel de administración",
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro",
        help_text="Fecha y hora en que el ciudadano se registró en el sistema",
    )

    objects = GestorCiudadano()

    USERNAME_FIELD = "correo_electronico"
    REQUIRED_FIELDS = ["nombre_completo", "numero_identificacion"]

    class Meta:
        verbose_name = "Ciudadano"
        verbose_name_plural = "Ciudadanos"
        db_table = "ciudadano_app_ciudadano"

    def __str__(self):
        return f"{self.nombre_completo} ({self.correo_electronico})"

    @property
    def is_active(self):
        """
        Indica si el usuario está activo.
        """
        return self.esta_activo

    def has_perm(self, perm, obj=None):
        """
        Verifica si el usuario tiene un permiso específico.
        """
        return True if self.is_staff else super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        """
        Verifica si el usuario tiene permisos para ver la aplicación app_label.
        """
        return True if self.is_staff else super().has_module_perms(app_label)
