from ciudadano_app.models import Ciudadano, AreaComunal, Reserva
from ciudadano_app.models.reserva.repositorio_reserva import RespositorioReserva


class ServicioReserva(RespositorioReserva):
    MAXIMO_RESERVAS = 3

    def ciudadano_supera_maximo_reservas(self, ciudadano: Ciudadano):
        return ciudadano.obtener_reservas_activas() > self.MAXIMO_RESERVAS

    def reservar_area_comunal(self, area_comunal: AreaComunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva, ciudadano: Ciudadano):
        if self.ciudadano_supera_maximo_reservas(ciudadano):

            return 0, False

        reserva = Reserva.objects.create(
            area_comunal=area_comunal,
            fecha_reserva=fecha_reserva,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            tipo_reserva=tipo_reserva,
            ciudadano=ciudadano
        )
        return reserva.obtener_id(), True
