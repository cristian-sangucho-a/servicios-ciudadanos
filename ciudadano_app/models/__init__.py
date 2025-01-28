"""
Inicializa el paquete de modelos para la aplicación ciudadano_app.
"""

# ciudadano_app/models/__init__.py

# Importaciones relativas desde submodulos
from .ciudadano.ciudadano import Ciudadano
from .ciudadano.gestor_ciudadano import GestorCiudadano
from .reserva import Reserva
from .area_comunal import AreaComunal
from .reporte.tipo_reporte import TipoReporte
from .reporte.reporte import Reporte

__all__ = [
    "Ciudadano",
    "GestorCiudadano",
    "Reserva",
    "AreaComunal",
    "Reporte",
    "TipoReporte"
]
default_app_config = 'ciudadano_app.apps.CiudadanoAppConfig'