"""
Inicializa el paquete de modelos para la aplicación ciudadano_app.
"""

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.ciudadano.gestor_ciudadano import GestorCiudadano
from ciudadano_app.models.reserva.reserva import Reserva

__all__ = ["Ciudadano", "GestorCiudadano", "Reserva"]
from ciudadano_app.models.reporte.tipo_reporte import TipoReporte
from ciudadano_app.models.reporte.reporte import Reporte

__all__ = [
    "Ciudadano",
    "TipoReporte",
    "Reporte",
    "RepositorioDeReporte",
    "ServicioDeReporte",
]
