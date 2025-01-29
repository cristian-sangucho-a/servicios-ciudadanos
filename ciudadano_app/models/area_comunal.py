from datetime import time, datetime, timedelta
from django.db import models

from entidad_municipal_app.models.espacio_publico import EspacioPublico


class AreaComunal(models.Model):
    nombre_area = models.CharField(
        max_length=100,
        help_text="Nombre del área comunal",
        default="Área Comunal"
    )
    hora_de_apertura = models.TimeField(
        help_text="Hora de apertura del área comunal",
        default=time(7, 0, 0)
    )
    hora_de_cierre = models.TimeField(
        help_text="Hora de cierre del área comunal",
        default=time(19, 0, 0)
    )
    espacio_publico = models.ForeignKey(
        EspacioPublico,
        on_delete=models.CASCADE,
        help_text="Espacio público al que pertenece el área comunal",
        related_name = 'areas_comunales'
    )


