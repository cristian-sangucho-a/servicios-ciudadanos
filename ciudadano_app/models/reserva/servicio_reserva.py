from ciudadano_app.models import Ciudadano, AreaComunal, Reserva
from ciudadano_app.models.reserva.repositorio_reserva import RespositorioReserva
from ciudadano_app.models.servicio_notificacion_correo import ServicioNotificacionPorCorreo
from entidad_municipal_app.models import EspacioPublico


class ServicioReserva(RespositorioReserva):
    """
    Clase que implementa la lógica del servicio de reservas para áreas comunales.

    Attributes:
        MAXIMO_RESERVAS (int): El número máximo de reservas activas permitidas por ciudadano.
    """

    MAXIMO_RESERVAS = 3

    def ciudadano_supera_maximo_reservas(self, ciudadano: Ciudadano):
        """
        Verifica si un ciudadano supera el número máximo de reservas activas permitidas.

        Args:
            ciudadano (Ciudadano): El ciudadano cuyas reservas se verificarán.

        Returns:
            bool: True si el ciudadano supera el límite de reservas activas, False en caso contrario.
        """
        return ciudadano.reservas.filter(estado_reserva='Activa').count() >= self.MAXIMO_RESERVAS

    def hay_areas_comunales_disponibles(self, espacio_publico):
        """
        Verifica si existen áreas comunales disponibles en un espacio público.

        Args:
            espacio_publico (EspacioPublico): El espacio público donde se buscarán las áreas comunales.

        Returns:
            bool: True si hay áreas comunales disponibles, False en caso contrario.
        """
        return AreaComunal.objects.filter(espacio_publico=espacio_publico).count() > 0

    def obtener_area_comunal(self, id_area_comunal):
        """
        Obtiene un área comunal por su ID.

        Args:
            id_area_comunal (int): El ID del área comunal a obtener.

        Returns:
            AreaComunal: La instancia del área comunal correspondiente al ID.
        """
        return AreaComunal.objects.get(id=id_area_comunal)

    def obtener_reserva_por_id(self, id_reserva):
        """
        Obtiene una reserva por su ID.

        Args:
            id_reserva (int): El ID de la reserva a obtener.

        Returns:
            Reserva: La instancia de la reserva correspondiente al ID.
        """
        return Reserva.objects.get(id=id_reserva)

    def cancelar_reserva(self, id_reserva, ciudadano):
        """
        Cancela una reserva realizada por un ciudadano.

        Args:
            id_reserva (int): El ID de la reserva a cancelar.
            ciudadano (Ciudadano): El ciudadano que solicita la cancelación.

        Steps:
            - Verifica que la reserva pertenezca al ciudadano.
            - Si es una reserva privada, envía notificaciones de cancelación a los invitados.
            - Actualiza el estado de la reserva a "Cancelada".

        Returns:
            bool: True si la reserva se canceló correctamente, False si no pertenece al ciudadano.
        """
        reserva = self.obtener_reserva_por_id(id_reserva)
        if reserva.ciudadano != ciudadano:
            return False

        if reserva.tipo_reserva == "privado":
            servicio_notificion_correo = ServicioNotificacionPorCorreo()
            servicio_notificion_correo.enviar_cancelacion(reserva)

        reserva.estado_reserva = 'Cancelada'
        reserva.save()
        return True

    def agregar_correos_invitados_a_reserva(self, id_reserva, correos_invitados):
        """
        Agrega correos de invitados a una reserva existente.

        Args:
            id_reserva (int): El ID de la reserva a la que se agregarán los correos.
            correos_invitados (str): Los correos de los invitados separados por comas.

        Steps:
            - Obtiene la reserva por su ID.
            - Actualiza el campo de correos de invitados.
            - Guarda los cambios en la base de datos.

        Returns:
            bool: True si los correos se agregaron correctamente.
        """
        reserva = self.obtener_reserva_por_id(id_reserva)
        reserva.correos_invitados = correos_invitados
        reserva.save()
        return True

    def obtener_reservas_activas_ciudadano(self, ciudadano):
        """
        Obtiene las reservas activas de un ciudadano.

        Args:
            ciudadano (Ciudadano): El ciudadano cuyas reservas activas se buscarán.

        Returns:
            QuerySet: Un conjunto de reservas activas asociadas al ciudadano.
        """
        return ciudadano.reservas.filter(estado_reserva='Activa')

    def obtener_reservas_area_comunal(self, area_comunal, fecha):
        """
        Obtiene las reservas activas de un área comunal en una fecha específica.

        Args:
            area_comunal (AreaComunal): El área comunal cuyas reservas se buscarán.
            fecha (datetime.date): La fecha para la cual se buscarán las reservas.

        Returns:
            QuerySet: Un conjunto de reservas activas asociadas al área comunal y la fecha.
        """
        return area_comunal.reservas.filter(fecha_reserva=fecha, estado_reserva='Activa')

    def reservar_area_comunal(self, area_comunal: AreaComunal, fecha_reserva, hora_inicio,
                              hora_fin, tipo_reserva,
                              ciudadano: Ciudadano, correos_invitados):
        """
        Realiza una reserva para un área comunal.

        Args:
            area_comunal (AreaComunal): El área comunal a reservar.
            fecha_reserva (datetime.date): La fecha de la reserva.
            hora_inicio (datetime.time): La hora de inicio de la reserva.
            hora_fin (datetime.time): La hora de fin de la reserva.
            tipo_reserva (str): El tipo de reserva ("pública" o "privada").
            ciudadano (Ciudadano): El ciudadano que realiza la reserva.
            correos_invitados (str): Los correos de los invitados separados por comas.

        Steps:
            - Verifica si el ciudadano supera el límite de reservas activas.
            - Crea una nueva reserva con los datos proporcionados.
            - Verifica si ya existe una reserva para el mismo horario.
            - Guarda la reserva en la base de datos.
            - Si es una reserva privada, envía invitaciones por correo.

        Returns:
            tuple: (ID de la reserva, bool) indicando si la reserva fue exitosa.
        """
        if self.ciudadano_supera_maximo_reservas(ciudadano):
            return 0, False
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
        if not self.existe_reserva(reserva):
            reserva.save()
        else:
            return 0, False
        if tipo_reserva == 'privado':
            servicio_notificion_correo = ServicioNotificacionPorCorreo()
            servicio_notificion_correo.enviar_invitacion(reserva)
        return reserva.obtener_id(), True

    def existe_reserva(self, reserva):
        """
        Verifica si ya existe una reserva para el mismo horario y área comunal.

        Args:
            reserva (Reserva): La reserva a verificar.

        Returns:
            bool: True si ya existe una reserva activa para el mismo horario, False en caso contrario.
        """
        return Reserva.objects.filter(area_comunal=reserva.area_comunal, fecha_reserva=reserva.fecha_reserva,
                                       hora_inicio=reserva.hora_inicio, hora_fin=reserva.hora_fin,
                                       estado_reserva='Activa').exists()

    def cancelar_reserva_privada(self, id_reserva, ciudadano):
        """
        Cancela una reserva privada y notifica a los invitados.

        Args:
            id_reserva (int): El ID de la reserva privada a cancelar.
            ciudadano (Ciudadano): El ciudadano que solicita la cancelación.

        Steps:
            - Verifica que la reserva pertenezca al ciudadano.
            - Actualiza el estado de la reserva a "Cancelada".
            - Envía notificaciones de cancelación a los invitados.

        Returns:
            bool: True si la reserva se canceló correctamente, False si no pertenece al ciudadano.
        """
        reserva = self.obtener_reserva_por_id(id_reserva)
        if reserva.ciudadano != ciudadano:
            return False
        reserva.estado_reserva = 'Cancelada'
        reserva.save()
        servicio_notificion_correo = ServicioNotificacionPorCorreo()
        servicio_notificion_correo.enviar_cancelacion(reserva)
        return True

    def obtener_espacios_publicos(self):
        """
        Obtiene todos los espacios públicos disponibles.

        Returns:
            QuerySet: Un conjunto de todos los espacios públicos registrados.
        """
        return EspacioPublico.objects.all()

    def obtener_areas_comunales_por_espacio(self, espacio_publico_id):
        """
        Obtiene todas las áreas comunales asociadas a un espacio público.

        Args:
            espacio_publico_id (int): El ID del espacio público.

        Returns:
            QuerySet: Un conjunto de áreas comunales asociadas al espacio público.
        """
        return AreaComunal.objects.filter(espacio_publico_id=espacio_publico_id)