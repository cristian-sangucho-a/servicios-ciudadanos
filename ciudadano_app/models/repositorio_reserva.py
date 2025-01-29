from abc import ABC, abstractmethod
from typing import Tuple

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano


class RespositorioReserva(ABC):

    @abstractmethod
    def ciudadano_supera_maximo_reservas(self, ciudadano: Ciudadano) -> bool:
        pass

    @abstractmethod
    def reservar_area_comunal(self, area_comunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva, ciudadano) -> Tuple[int, bool]:
        pass