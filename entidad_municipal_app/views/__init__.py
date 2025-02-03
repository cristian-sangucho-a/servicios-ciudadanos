from .dashboard import dashboard_entidad
from .login import login_entidad
from .bienvenida import bienvenida_entidad
from .eventos.gestor_eventos import gestor_eventos
from .eventos.evento import evento
from .eventos.editar_evento import editar_evento
from .eventos.crear_evento import crear_evento



__all__ = [
    'dashboard_entidad',
    'login_entidad',
    'bienvenida_entidad',
    'gestor_eventos',
    'evento',
    'editar_evento',
    'crear_evento',
]
