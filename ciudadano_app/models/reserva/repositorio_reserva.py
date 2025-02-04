from abc import ABC, abstractmethod
from typing import Tuple

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano


class RespositorioReserva(ABC):

    @abstractmethod
    def ciudadano_supera_maximo_reservas(self, ciudadano: Ciudadano) -> bool:
        pass

    @abstractmethod
    def reservar_area_comunal(self, area_comunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva, ciudadano,
                              correos_invitados) -> Tuple[int, bool]:
        pass

    @abstractmethod
    def hay_areas_comunales_disponibles(self, espacio_publico) -> bool:
        pass

    # Vamos a quemar datos en la bd
    # @abstractmethod
    # def agregar_area_comunal(self, area_comunal, espacio_publico):
    #     pass


    # Puede ir en un servicio especializado en areas comunales
    @abstractmethod
    def obtener_area_comunal(self, id_area_comunal):
        pass

    @abstractmethod
    def obtener_reserva_por_id(self, id_reserva):
        pass

    @abstractmethod
    def cancelar_reserva(self, id_reserva, ciudadano) -> bool:
        pass

    # Esto puede ir en el controlador/servicio notificacion
    # @abstractmethod
    # def enviar_invitacion(self, reserva) -> bool:
    #     pass

    @abstractmethod
    def agregar_correos_invitados_a_reserva(self, id_reserva, correos_invitados):
        pass

    # Esto puede ir en el controlador/servicio notificacion
    # @abstractmethod
    # def enviar_cancelacion(self, reserva) -> bool:
    #     pass
