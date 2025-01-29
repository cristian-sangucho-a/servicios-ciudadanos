from abc import ABC, abstractmethod
from ciudadano_app.models.reporte.reporte import Reporte


class RepositorioDeReporteMunicipal(ABC):
    """
    Interfaz abstracta que define las operaciones para el repositorio de reportes municipales.
    """

    @abstractmethod
    def obtener_por_id(self, id_reporte: int):
        """
        Obtiene un reporte municipal por su ID.

        Args:
            id_reporte (int): ID del reporte municipal a buscar

        Returns:
            ReporteMunicipal: Instancia del reporte municipal o None si no existe
        """
        pass

    @abstractmethod
    def obtener_todos(self):
        """
        Obtiene todos los reportes municipales.

        Returns:
            list[ReporteMunicipal]: Lista de todos los reportes municipales
        """
        pass

    @abstractmethod
    def obtener_por_estado(self, estado: str):
        """
        Obtiene reportes municipales filtrados por estado.

        Args:
            estado (str): Estado de los reportes a buscar

        Returns:
            list[ReporteMunicipal]: Lista de reportes municipales en el estado especificado
        """
        pass

    @abstractmethod
    def crear(self, reporte_ciudadano: Reporte):
        """
        Crea un nuevo reporte municipal a partir de un reporte ciudadano.

        Args:
            reporte_ciudadano (Reporte): Reporte ciudadano base

        Returns:
            ReporteMunicipal: Nuevo reporte municipal creado
        """
        pass

    @abstractmethod
    def actualizar(self, reporte_municipal):
        """
        Actualiza un reporte municipal existente.

        Args:
            reporte_municipal (ReporteMunicipal): Reporte municipal a actualizar

        Returns:
            ReporteMunicipal: Reporte municipal actualizado
        """
        pass

    @abstractmethod
    def eliminar(self, id_reporte: int):
        """
        Elimina un reporte municipal por su ID.

        Args:
            id_reporte (int): ID del reporte municipal a eliminar

        Returns:
            bool: True si se eliminó correctamente, False si no existía
        """
        pass