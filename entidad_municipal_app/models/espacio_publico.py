from django.db import models
class EspacioPublico(models.Model):
    """
    Modelo para representar un espacio público.
    """
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre del espacio público",
        default="Espacio Público"
    )
