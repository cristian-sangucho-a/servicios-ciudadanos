"""
Modelos de la aplicación de entidad municipal.
"""

from .EntidadMunicipal import EntidadMunicipal
from .evento_municipal import EventoMunicipal
from .registro_asistencia import RegistroAsistencia
from .canales.canal_informativo import *
from .canales.noticia import *

__all__ = ['EntidadMunicipal', 'EventoMunicipal', 'RegistroAsistencia','CanalInformativo','Suscripcion','Noticia','Reaccion','Comentario']
