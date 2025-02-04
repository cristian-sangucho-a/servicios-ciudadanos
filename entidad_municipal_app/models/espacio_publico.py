from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from entidad_municipal_app.models import EntidadMunicipal

class EspacioPublico(models.Model):
    """Modelo para representar un espacio público."""

    nombre = models.CharField(
        max_length=255,
        help_text="Nombre del espacio público",
        default="Espacio Público"
    )
    direccion = models.CharField(
        max_length=255,
        verbose_name='Lugar',
        help_text='Ubicación donde se encuentra el espacio público'
    )
    descripcion = models.TextField()

    entidad_municipal = models.ForeignKey(
        'entidad_municipal_app.EntidadMunicipal',
        on_delete=models.CASCADE,
        verbose_name=_("Entidad Municipal"),
        related_name='espacios_publicos'
    )

    ESTADO_DISPONIBLE = 'DISPONIBLE'
    ESTADO_NO_DISPONIBLE = 'NO_DISPONIBLE'

    ESTADOS_DISPONIBILIDAD = [
        (ESTADO_DISPONIBLE, 'Disponible'),
        (ESTADO_NO_DISPONIBLE, 'No Disponible'),
    ]

    estado_espacio_publico = models.CharField(
        max_length=20,
        choices=ESTADOS_DISPONIBILIDAD,
        default=ESTADO_DISPONIBLE,
        help_text="Estado del espacio público en la fecha especificada"
    )

    AFECTADO = "AFECTADO"
    NO_AFECTADO = "NO_AFECTADO"
    ESTADO_CHOICES = [
        (AFECTADO, 'Afectado'),
        (NO_AFECTADO, 'No Afectado'),
    ]

    estado_incidente_espacio = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=NO_AFECTADO,
        help_text="Estado del espacio público"
    )

    @staticmethod
    def obtener_espacios_disponibles(query=None, filtrar_disponibles=False):
        espacios = EspacioPublico.objects.filter(estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE)

        if query:
            espacios = espacios.filter(
                Q(nombre__icontains=query) | Q(direccion__icontains=query)
            )

        if filtrar_disponibles == 'False':
            espacios = EspacioPublico.objects.all()

        return espacios

    def __str__(self):
        return self.nombre

    def obtener_id(self):
        return self.id

    def obtener_nombre(self):
        return self.nombre

