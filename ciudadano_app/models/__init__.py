"""
Inicializa el paquete de modelos para la aplicación ciudadano_app.
"""

from .ciudadano import Ciudadano
from .gestor_ciudadano import GestorCiudadano
from .reserva import Reserva
from .area_comunal import AreaComunal
__all__ = ["Ciudadano", "GestorCiudadano", "Reserva",'AreaComunal']
from .TipoReporte import TipoReporte
from .Reporte import Reporte

__all__ = [
    "Ciudadano",
    "TipoReporte",
    "Reporte",
    "RepositorioDeReporte",
    "ServicioDeReporte",
]
