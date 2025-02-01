from .dashboard import dashboard_entidad
from .login import login_entidad
from .bienvenida import bienvenida_entidad
from .eventos.lista_eventos import lista_eventos
from .reportes.lista_reportes import lista_todos_reportes
from .reportes.lista_reportes_por_departamento import lista_reportes_por_departamento
from .reportes.postergar_reporte import postergar_reporte
from .reportes.resolver_reporte import resolver_reporte

__all__ = [
    'dashboard_entidad',
    'login_entidad',
    'bienvenida_entidad',
    'lista_eventos',
    'lista_todos_reportes',
    'lista_reportes_por_departamento',
    'postergar_reporte',
    'resolver_reporte'
]