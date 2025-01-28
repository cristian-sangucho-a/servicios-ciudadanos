from django.db import models

from ciudadano_app.models import Ciudadano, AreaComunal, Reserva


class ServicioReserva(models.Model):
    MAXIMO_RESERVAS = 3

    def ciudadano_supera_maximo_reservas(self, ciudadano: Ciudadano):
        return ciudadano.obtener_reservas_activas() > self.MAXIMO_RESERVAS