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
        help_text="Entidad municipal a la que pertenece el espacio público"
    )