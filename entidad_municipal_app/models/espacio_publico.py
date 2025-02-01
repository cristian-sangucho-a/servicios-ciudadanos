from django.db import models
from entidad_municipal_app.models import EntidadMunicipal
class EspacioPublico(models.Model):
    """
    Modelo para representar un espacio público.
    """
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre del espacio público",
        default="Espacio Público"
    )
    entidad_municipal = models.ForeignKey(
        EntidadMunicipal,
        on_delete=models.CASCADE,
        help_text="Entidad municipal a la que pertenece el espacio público",
        related_name = 'espacios_publicos'
    )

    direccion = models.CharField(
        max_length=200,
        verbose_name='Lugar',
        help_text='Ubicación donde se encuentra el espacio público'
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

    def mostrar_espacios_disponibles(fecha):
        """
        Retorna los espacios públicos disponibles en la fecha especificada
        """
        return EspacioPublico.objects.filter(
            estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE
    )
