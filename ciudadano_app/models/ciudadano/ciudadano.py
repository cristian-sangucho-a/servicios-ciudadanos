"""
Modelo principal de Ciudadano.
"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from ciudadano_app.models.ciudadano.gestor_ciudadano import GestorCiudadano


class Ciudadano(AbstractBaseUser):
    """
    Modelo que representa a un ciudadano en el sistema municipal.
    Extiende el modelo base de usuario de Django para incluir campos específicos.
    """

    correo_electronico: models.EmailField = models.EmailField(
        unique=True,
        verbose_name="Correo Electrónico",
        help_text="Dirección de correo electrónico del ciudadano",
    )

    nombre_completo: models.CharField = models.CharField(
        max_length=120,
        verbose_name="Nombre Completo",
        help_text="Nombre completo del ciudadano",
    )

    numero_identificacion: models.CharField = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Número de Identificación",
        help_text="Número de documento de identidad del ciudadano",
    )

    esta_activo: models.BooleanField = models.BooleanField(
        default=True,
        verbose_name="¿Está Activo?",
        help_text="Indica si el ciudadano puede acceder al sistema",
    )

    es_staff: models.BooleanField = models.BooleanField(
        default=False,
        verbose_name="¿Es Personal Administrativo?",
        help_text="Indica si el ciudadano puede acceder al panel de administración",
    )

    fecha_registro: models.DateTimeField = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Registro",
        help_text="Fecha y hora en que el ciudadano se registró en el sistema",
    )
    
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_admin: models.BooleanField = models.BooleanField(default=False)

    objects = GestorCiudadano()

    USERNAME_FIELD = "correo_electronico"
    EMAIL_FIELD = "correo_electronico"
    REQUIRED_FIELDS = ["nombre_completo", "numero_identificacion"]

    def obtener_nombre_completo(self):
        """Retorna el nombre completo del ciudadano"""
        return self.nombre_completo

    def obtener_correo_electronico(self):
        """Retorna el correo electrónico del ciudadano"""
        return self.correo_electronico

    def obtener_identificacion(self):
        """Retorna el número de identificación del ciudadano"""
        return self.numero_identificacion

    def __str__(self):
        """Retorna una representación en cadena del ciudadano"""
        return f"Ciudadano: {self.nombre_completo} ({self.correo_electronico})"
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def es_ciudadano(self):
        """Identifica que este usuario es un ciudadano"""
        return True

    class Meta:
        verbose_name = "Ciudadano"
        verbose_name_plural = "Ciudadanos"
        ordering = ["-fecha_registro"]