from abc import ABC, abstractmethod

from ciudadano_app.models.Reporte import Reporte


class RepositorioDeReporte(ABC):
    @abstractmethod
    def obtener_reportes_por_asunto(self, asunto: str):
        pass

    @abstractmethod
    def agregar_reporte(self, reporte: Reporte):
        pass

    @abstractmethod
    def actualziar_prioridad_de_reporte_por_asunto(self, asunto: str, prioridad: int):
        pass
