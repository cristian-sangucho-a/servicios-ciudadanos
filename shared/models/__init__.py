"""
Modelos de la aplicación de entidad municipal.
"""

from .reporte.tipo_reporte import TipoReporte
from .reporte.reporte import Reporte
from .reporte.repositorio_de_reporte import RepositorioDeReporte
from .reporte.servicio_de_reporte import ServicioDeReporte
from .reporte.repositorio_de_reporte_django import RepositorioDeReporteDjango
from .notificacion.servicio_de_notificacion import ServicioDeNotificacion
from .notificacion.notificacion import Notificacion
from .notificacion.sector import Sector

__all__ = [
    'Reporte',
    'RepositorioDeReporte',
    'TipoReporte',
    'ServicioDeReporte',
    'RepositorioDeReporteDjango',
    'ServicioDeNotificacion',
    'Notificacion',
    'Sector',
]
