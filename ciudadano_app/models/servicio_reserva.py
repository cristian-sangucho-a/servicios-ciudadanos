from django.db import models

from ciudadano_app.models import Ciudadano


class ControladorReserva:
    MAXIMO_RESERVAS = 3

    def ciudadano_no_supera_maximo_reservas(self, ciudadano: Ciudadano):
        return ciudadano.obtener_reservas_activas() < self.MAXIMO_RESERVAS

    def reervar_area_comunal(self, area_comunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva, ciudadano):
        pass
