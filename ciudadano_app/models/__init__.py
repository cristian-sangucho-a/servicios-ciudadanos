"""
Inicializa el paquete de modelos para la aplicación ciudadano_app.
"""

# ciudadano_app/models/__init__.py
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.ciudadano.gestor_ciudadano import GestorCiudadano
from ciudadano_app.models.area_comunal import AreaComunal
from ciudadano_app.models.reserva.reserva import Reserva
from shared.models.reporte.tipo_reporte import TipoReporte
from shared.models.reporte.reporte import Reporte

__all__ = [
    "Ciudadano",
    "GestorCiudadano",
    "Reserva",
    "AreaComunal",
    "Reporte",
    "TipoReporte"
]

