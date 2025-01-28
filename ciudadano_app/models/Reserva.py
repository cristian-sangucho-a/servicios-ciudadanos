from django.db import models
from ciudadano_app.models import Ciudadano


class Reserva(models.Model):
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)

