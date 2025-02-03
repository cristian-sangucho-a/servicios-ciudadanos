from ciudadano_app.models import Ciudadano, AreaComunal, Reserva
from ciudadano_app.models.reserva.repositorio_reserva import RespositorioReserva
from ciudadano_app.models.servicio_notificacion_correo import ServicioNotificacionPorCorreo
from entidad_municipal_app.models import EspacioPublico


class ServicioReserva(RespositorioReserva):
    MAXIMO_RESERVAS = 3

    def ciudadano_supera_maximo_reservas(self, ciudadano: Ciudadano):
        print(ciudadano.reservas.filter(estado_reserva='Activa').count())
        return ciudadano.reservas.filter(estado_reserva='Activa').count() > self.MAXIMO_RESERVAS

    def reservar_area_comunal(self, area_comunal: AreaComunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva,
                              ciudadano: Ciudadano):
        print(self.ciudadano_supera_maximo_reservas(ciudadano))
        if self.ciudadano_supera_maximo_reservas(ciudadano):
            return 0, False
        #TODO: verificar que el espacio publico al que pertenece el area comunal este libre para reservar
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

        if reserva.tipo_reserva == "privada":
            servicio_notificion_correo = ServicioNotificacionPorCorreo()
            servicio_notificion_correo.enviar_cancelacion(reserva)

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

    def obtener_reservas_area_comunal(self, area_comunal, fecha):
        return area_comunal.reservas.filter(fecha_reserva=fecha)

    def reservar(self, area_comunal: AreaComunal, fecha_reserva, hora_inicio,
                                                     hora_fin, tipo_reserva,
                                                     ciudadano: Ciudadano, correos_invitados):
        print(self.ciudadano_supera_maximo_reservas(ciudadano))
        if self.ciudadano_supera_maximo_reservas(ciudadano):
            print(self.ciudadano_supera_maximo_reservas(ciudadano))
            return 0, False

        #TODO: verificar que el espacio publico al que pertenece el area comunal este libre para reservar
        reserva = Reserva(
            area_comunal=area_comunal,
            fecha_reserva=fecha_reserva,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estado_reserva='Activa',
            tipo_reserva=tipo_reserva,
            ciudadano=ciudadano,
            correos_invitados=correos_invitados
        )
        reserva.save()
        if tipo_reserva == 'privado':
            servicio_notificion_correo = ServicioNotificacionPorCorreo()
            servicio_notificion_correo.enviar_invitacion(reserva)
        return reserva.obtener_id(), True


    def cancelar_reserva_privada(self, id_reserva, ciudadano):
        reserva = self.obtener_reserva_por_id(id_reserva)
        if reserva.ciudadano != ciudadano:
            return False
        reserva.estado_reserva = 'Cancelada'
        reserva.save()
        servicio_notificion_correo = ServicioNotificacionPorCorreo()
        servicio_notificion_correo.enviar_cancelacion(reserva)
        return True

    ##PARA RECUPERAR DATOS DESDE LA VISTA

    def obtener_espacios_publicos(self):
        return EspacioPublico.objects.all()

    def obtener_areas_comunales_por_espacio(self, espacio_publico_id):
        return AreaComunal.objects.filter(espacio_publico_id=espacio_publico_id)
