from django.db import models
from ciudadano_app.models import Ciudadano, AreaComunal


class Reserva(models.Model):
    area_comunal = models.OneToOneField(
        AreaComunal,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='+'
    )

    def obtener_id(self):
        return self.pk


    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)

