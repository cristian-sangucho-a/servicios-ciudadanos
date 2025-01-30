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

    es_staff = models.BooleanField(
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
        ordering = ["-fecha_registro"]

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

    def obtener_reservas_activas(self):
        """Retorna el número de reservas activas del ciudadano"""
        return self.reservas.filter(estado_reserva='Activa').count()