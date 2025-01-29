"""
Modelo para representar una entidad municipal.
"""
from django.db import models
from django.utils import timezone

class EntidadMunicipal(models.Model):
    """
    Representa una entidad municipal que puede organizar eventos.
    """
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre de la entidad municipal",
        default="Entidad Municipal"
    )
    direccion = models.CharField(
        max_length=200,
        help_text="Dirección física de la entidad",
        default="Dirección no especificada"
    )
    telefono = models.CharField(
        max_length=20,
        help_text="Número de teléfono de contacto",
        default="000-000-0000"
    )
    correo_electronico = models.EmailField(
        help_text="Correo electrónico de contacto",
        default="contacto@entidad.com"
    )
    fecha_registro = models.DateTimeField(
        help_text="Fecha de registro en el sistema",
        default=timezone.now
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Entidad Municipal"
        verbose_name_plural = "Entidades Municipales"