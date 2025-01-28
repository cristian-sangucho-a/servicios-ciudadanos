"""
Inicializa el paquete de modelos para la aplicación ciudadano_app.
"""

from .reserva import Reserva
from .area_comunal import AreaComunal

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.ciudadano.gestor_ciudadano import GestorCiudadano
from ciudadano_app.models.reserva import Reserva
from ciudadano_app.models.reporte.tipo_reporte import TipoReporte
from ciudadano_app.models.reporte.reporte import Reporte


__all__ = ["Ciudadano", "GestorCiudadano", "Reserva",'AreaComunal']


__all__ = [
    "Ciudadano",
    "Reporte",
]
