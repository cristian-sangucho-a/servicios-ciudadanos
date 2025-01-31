from ciudadano_app.models import Ciudadano, AreaComunal, Reserva
from ciudadano_app.models.reserva.repositorio_reserva import RespositorioReserva
from ciudadano_app.models.servicio_notificacion_correo import ServicioNotificacionPorCorreo


class ServicioReserva(RespositorioReserva):
    MAXIMO_RESERVAS = 3

    def ciudadano_supera_maximo_reservas(self, ciudadano: Ciudadano):
        return ciudadano.reservas.filter(estado_reserva='Activa').count() > self.MAXIMO_RESERVAS

    def reservar_area_comunal(self, area_comunal: AreaComunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva,
                              ciudadano: Ciudadano):
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

    def hay_areas_comunales_disponibles(self, espacio_publico):
        return AreaComunal.objects.filter(espacio_publico=espacio_publico).count() > 0

    def obtener_area_comunal(self, id_area_comunal):
        return AreaComunal.objects.get(id=id_area_comunal)

    def obtener_reserva_por_id(self, id_reserva):
        return Reserva.objects.get(id=id_reserva)

    def cancelar_reserva(self, id_reserva, ciudadano):
        reserva = self.obtener_reserva_por_id(id_reserva)
        if reserva.ciudadano != ciudadano:
            return False
        reserva.estado_reserva = 'Cancelada'
        reserva.save()
        return True

    def agregar_correos_invitados_a_reserva(self, id_reserva, correos_invitados):
        reserva = self.obtener_reserva_por_id(id_reserva)
        reserva.correos_invitados = correos_invitados
        reserva.save()
        return True

    def obtener_reservas_activas_ciudadano(self, ciudadano):
        return ciudadano.reservas.filter(estado_reserva='Activa')

    def obtener_reservas_area_comunal(self, area_comunal):
        return area_comunal.reservas.all()

    def reservar_area_comunal_para_actividad_privada(self, area_comunal: AreaComunal, fecha_reserva, hora_inicio,
                                                     hora_fin, tipo_reserva,
                                                     ciudadano: Ciudadano, correos_invitados):
        try:
            id_reserva, fue_reservado = self.reservar_area_comunal(area_comunal, fecha_reserva, hora_inicio, hora_fin,
                                                                   tipo_reserva, ciudadano)
        except Exception:
            return None, False
        reserva_realizada = self.obtener_reserva_por_id(id_reserva)
        reserva_realizada.agregar_correos_invitados(correos_invitados)
        servicio_notificion_correo = ServicioNotificacionPorCorreo()
        servicio_notificion_correo.enviar_invitacion(reserva_realizada)
        return id_reserva, fue_reservado

    def cancelar_reserva_creada(self, id_reserva, ciudadano):
        reserva = self.obtener_reserva_por_id(id_reserva)
        if reserva.ciudadano != ciudadano:
            return False
        reserva.estado_reserva = 'Cancelada'
        reserva.save()
        servicio_notificion_correo = ServicioNotificacionPorCorreo()
        servicio_notificion_correo.enviar_cancelacion(reserva)
        return True