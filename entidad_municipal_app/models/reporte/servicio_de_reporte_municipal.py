from django.core.exceptions import ValidationError
from .repositorio_de_reporte_municipal import RepositorioDeReporteMunicipal


class ServicioDeReporteMunicipal:
    """
    Servicio que implementa la lógica de negocio para los reportes municipales.
    """

    def __init__(self, repositorio: RepositorioDeReporteMunicipal):
        """
        Inicializa el servicio con un repositorio de reportes municipales.

        Args:
            repositorio (RepositorioDeReporteMunicipal): Repositorio a utilizar
        """
        self.repositorio = repositorio

    def crear_reporte_municipal(self, reporte_ciudadano):
        """
        Crea un nuevo reporte municipal a partir de un reporte ciudadano.

        Args:
            reporte_ciudadano (Reporte): Reporte ciudadano base

        Returns:
            ReporteMunicipal: Nuevo reporte municipal
        """
        return self.repositorio.crear(reporte_ciudadano)

    def actualizar_estado(self, id_reporte: int, nuevo_estado: str):
        """
        Actualiza el estado de un reporte municipal.

        Args:
            id_reporte (int): ID del reporte a actualizar
            nuevo_estado (str): Nuevo estado a establecer

        Raises:
            ValidationError: Si el estado no es válido o el reporte no existe
        """
        reporte = self.repositorio.obtener_por_id(id_reporte)
        if not reporte:
            raise ValidationError(f"No existe reporte con ID {id_reporte}")

        reporte.cambiar_estado(nuevo_estado)
        self.repositorio.actualizar(reporte)

    def registrar_evidencia(self, id_reporte: int, evidencia: str):
        """
        Registra evidencia en un reporte municipal.

        Args:
            id_reporte (int): ID del reporte
            evidencia (str): Evidencia a registrar

        Raises:
            ValidationError: Si el reporte no existe
        """
        reporte = self.repositorio.obtener_por_id(id_reporte)
        if not reporte:
            raise ValidationError(f"No existe reporte con ID {id_reporte}")

        reporte.registrar_evidencia(evidencia)
        self.repositorio.actualizar(reporte)

    def obtener_reportes_por_estado(self, estado: str):
        """
        Obtiene todos los reportes en un estado específico.

        Args:
            estado (str): Estado de los reportes a buscar

        Returns:
            list[ReporteMunicipal]: Lista de reportes en el estado especificado
        """
        return self.repositorio.obtener_por_estado(estado)
