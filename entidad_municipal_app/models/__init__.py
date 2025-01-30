"""
Modelos de la aplicación de entidad municipal.
"""

from .EntidadMunicipal import EntidadMunicipal
from .evento_municipal import EventoMunicipal
from .registro_asistencia import RegistroAsistencia

from .canales.canal_informativo import CanalInformativo, Suscripcion
from .canales.noticia import Noticia
from .canales.reaccion import Reaccion
from .canales.comentario import Comentario

__all__ = ['EntidadMunicipal', 'EventoMunicipal', 'RegistroAsistencia','CanalInformativo','Suscripcion','Noticia','Reaccion','Comentario','ReporteMunicipal', 'Departamento']
