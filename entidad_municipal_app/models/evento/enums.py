"""
Enums para los estados de eventos, registros y espacios públicos.
"""
from enum import Enum

class EstadoEvento(Enum):
    PROGRAMADO = 'PROGRAMADO'
    EN_CURSO = 'EN_CURSO'
    FINALIZADO = 'FINALIZADO'
    CANCELADO = 'CANCELADO'

    @classmethod
    def choices(cls):
        return [(estado.value, estado.name.title()) for estado in cls]

class EstadoRegistro(Enum):
    INSCRITO = 'INSCRITO'
    EN_ESPERA = 'EN_ESPERA'
    CANCELADO = 'CANCELADO'
    
    @classmethod
    def choices(cls):
        return [(estado.value, estado.name.title()) for estado in cls]
    
    @staticmethod
    def determinar_estado(cupos_disponibles):
        return EstadoRegistro.INSCRITO.value if cupos_disponibles > 0 else EstadoRegistro.EN_ESPERA.value

class EstadoAsistencia(Enum):
    PENDIENTE = 'PENDIENTE'
    ASISTIO = 'ASISTIO'
    NO_ASISTIO = 'NO_ASISTIO'
    
    @classmethod
    def choices(cls):
        return [(estado.value, estado.name.title()) for estado in cls]

class EstadoEspacioPublico(Enum):
    DISPONIBLE = 'DISPONIBLE'
    NO_DISPONIBLE = 'NO_DISPONIBLE'
    AFECTADO = 'AFECTADO'

    @classmethod
    def choices(cls):
        return [(estado.value, estado.name.title()) for estado in cls]
