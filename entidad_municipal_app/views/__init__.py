from .dashboard import dashboard_entidad
from .login import login_entidad
from .bienvenida import bienvenida_entidad
from .eventos.gestor_eventos import gestor_eventos
from .eventos.evento import evento

from .reportes.lista_reportes import lista_todos_reportes
from .reportes.postergar_reporte import postergar_reporte
from .reportes.resolver_reporte import resolver_reporte
from .reportes.agregar_evidencia import agregar_evidencia

__all__ = [
    'dashboard_entidad',
    'login_entidad',
    'bienvenida_entidad',
    'gestor_eventos',
    'evento',
    'lista_todos_reportes',
    'postergar_reporte',
    'resolver_reporte',
    'agregar_evidencia'
]
