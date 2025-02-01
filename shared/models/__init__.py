"""
Modelos de la aplicación de entidad municipal.
"""

from .reporte.reporte import Reporte
from .reporte.repositorio_de_reporte import RepositorioDeReporte
from .reporte.tipo_reporte import TipoReporte
from .reporte.servicio_de_reporte import ServicioDeReporte
from .reporte.repositorio_de_reporte_django import RepositorioDeReporteDjango
from .notificacion.notificacion import Notificacion

__all__ = ['Reporte', 'RepositorioDeReporte', 'TipoReporte', 'ServicioDeReporte', 'RepositorioDeReporteDjango', 'Notificacion']

