from threading import Lock
from django.db import transaction
from shared.models.reporte.repositorio_de_reporte_django import RepositorioDeReporteDjango
from .repositorio_de_reporte_municipal import RepositorioDeReporteMunicipal
from .reporte_municipal import ReporteMunicipal

class RepositorioDeReporteMunicipalDjango(RepositorioDeReporteMunicipal):
    """
    Implementación de Django del repositorio de reportes municipales con el patrón Singleton.
    """

    _instance = None
    _lock = Lock()  # Evita problemas en entornos multihilo

    def __new__(cls, *args, **kwargs):
        """
        Implementa el patrón Singleton: Asegura que solo haya una instancia de esta clase.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """
        Inicializa el repositorio solo una vez.
        Se crean automáticamente los Reportes Municipales a partir de los reportes ciudadanos disponibles.
        """
        if not hasattr(self, "_initialized"):
            self.repositorio_reporte_ciudadano = RepositorioDeReporteDjango()
            self.inicializar_reportes_municipales()
            self._initialized = True

    def inicializar_reportes_municipales(self):
        """
        Crea automáticamente reportes municipales a partir de los reportes ciudadanos.
        """
        reportes_ciudadanos = self.repositorio_reporte_ciudadano.obtener_reportes_ordenados_prioridad()

        for reporte_ciudadano in reportes_ciudadanos:
                self.crear(reporte_ciudadano)

    def obtener_por_id(self, id_reporte: int):
        """
        Obtiene un reporte municipal por su ID usando Django ORM.
        """
        try:
            return ReporteMunicipal.objects.get(id=id_reporte)
        except ReporteMunicipal.DoesNotExist:
            return None

    def obtener_todos(self):
        """
        Obtiene todos los reportes municipales usando Django ORM.
        """
        return list(ReporteMunicipal.objects.all())

    def obtener_por_estado(self, estado: str):
        """
        Obtiene reportes municipales por estado usando Django ORM.
        """
        return list(ReporteMunicipal.objects.filter(estado=estado))

    @transaction.atomic
    def crear(self, reporte_ciudadano):
        """
        Crea un nuevo reporte municipal usando Django ORM.
        """
        reporte_municipal = ReporteMunicipal.objects.create(
            reporte_ciudadano=reporte_ciudadano,
            estado="asignado",
            evidencia=None
        )
        reporte_municipal.save()
        return reporte_municipal

    @transaction.atomic
    def actualizar(self, reporte_municipal):
        """
        Actualiza un reporte municipal usando Django ORM.
        """
        reporte_municipal.save()
        return reporte_municipal

    def eliminar(self, id_reporte: int):
        """
        Elimina un reporte municipal usando Django ORM.
        """
        try:
            reporte = ReporteMunicipal.objects.get(id=id_reporte)
            reporte.delete()
            return True
        except ReporteMunicipal.DoesNotExist:
            return False
