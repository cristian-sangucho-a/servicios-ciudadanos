from django.db import models
from ciudadano_app.models import Ciudadano, AreaComunal


class Reserva(models.Model):
    area_comunal = models.OneToOneField(
        AreaComunal,
        on_delete=models.CASCADE,
        primary_key=True,
    )


    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)

