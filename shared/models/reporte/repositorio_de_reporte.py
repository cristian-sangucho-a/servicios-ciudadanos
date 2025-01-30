from abc import ABC, abstractmethod

# Importación del modelo Reporte.
from .reporte import Reporte


class RepositorioDeReporte(ABC):
    """
    Clase abstracta que define la interfaz para el repositorio de reportes.

    Esta interfaz establece los métodos básicos para interactuar con los reportes en la base de datos,
    asegurando que cualquier implementación de esta clase provea funcionalidades específicas.
    """

    @abstractmethod
    def obtener_reportes_por_asunto(self, asunto: str):
        """
        Método abstracto para obtener reportes basados en su asunto.

        Args:
            asunto (str): El asunto del reporte para filtrar los reportes en la base de datos.

        Returns:
            Debería retornar una lista de instancias de Reporte que coincidan con el asunto dado.
        """
        pass

    @abstractmethod
    def agregar_reporte(self, reporte: Reporte):
        """
        Método abstracto para agregar un nuevo reporte a la base de datos.

        Args:
            reporte (Reporte): La instancia del reporte a agregar.

        Returns:
            Debería realizar la inserción del reporte en la base de datos y retornar algún indicador de éxito o fracaso.
        """
        pass

    @abstractmethod
    def actualizar_prioridad_de_reporte_por_asunto(self, asunto: str, prioridad: int):
        """
        Método abstracto para actualizar la prioridad de un reporte específico identificado por su asunto.

        Args:
            asunto (str): El asunto del reporte cuya prioridad necesita ser actualizada.
            prioridad (int): El nuevo valor de prioridad para el reporte.

        Returns:
            Debería actualizar la prioridad del reporte en la base de datos y retornar algún indicador de éxito o fracaso.
        """
        pass
