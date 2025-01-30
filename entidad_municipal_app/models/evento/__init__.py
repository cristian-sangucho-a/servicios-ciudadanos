"""
Modelos relacionados con eventos municipales.
"""

from .evento_municipal import EventoMunicipal, ErrorGestionEventos
from .registro_asistencia import RegistroAsistencia

__all__ = ['EventoMunicipal', 'RegistroAsistencia', 'ErrorGestionEventos']
