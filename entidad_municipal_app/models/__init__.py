"""
Modelos de la aplicación de entidad municipal.
"""

from .EntidadMunicipal import EntidadMunicipal
from .evento_municipal import EventoMunicipal
from .registro_asistencia import RegistroAsistencia
from .reporte.reporte_municipal import ReporteMunicipal
from .departamento.departamento import Departamento

__all__ = ['EntidadMunicipal', 'EventoMunicipal', 'RegistroAsistencia','ReporteMunicipal', 'Departamento']

