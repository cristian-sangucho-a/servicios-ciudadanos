from datetime import time

from django.db import models

class AreaComunal(models.Model):
    nombre_area = models.CharField(
        max_length=100,
        help_text="Nombre del área comunal",
        default="Área Comunal"
    )
    hora_de_apertura = models.TimeField(
        help_text="Hora de apertura del área comunal",
        default= time(7, 0, 0),
        null=True
    )
    hora_de_cierre = models.TimeField(
        help_text="Hora de cierre del área comunal",
        default=time(20, 0, 0),
        null=True
    )


