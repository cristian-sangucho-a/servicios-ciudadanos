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
        help_text="Dirección del espacio público",
        default="Dirección no especificada"
    )

    disponibilidad = models.BooleanField(
    default=True
    )

    def get_direccion(self):
        """
        Obtiene el lugar del evento.
        """
        return self.direccion
    def esta_disponible(self):
        """
        Devuelve True si el espacio público está disponible, False si está ocupado.
        """
        return self.disponibilidad

    def cambiar_disponibilidad(self):
        """
        Cambia la disponibilidad del espacio público.
        """
        self.disponibilidad = not self.disponibilidad
        self.save()

    def __str__(self):
        return f"{self.nombre} - {'Disponible' if self.esta_disponible() else 'Ocupado'}"

    class Meta:
        verbose_name = "Espacio Público"
        verbose_name_plural = "Espacios Públicos"

