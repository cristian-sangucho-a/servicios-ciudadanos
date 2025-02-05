"""
Excepciones personalizadas para la gestión de eventos.
"""

class ErrorGestionEventos(Exception):
    """Excepción base para errores en la gestión de eventos municipales."""
    pass

class EventoNoDisponibleError(ErrorGestionEventos):
    """Se lanza cuando se intenta operar con un evento que no está disponible."""
    pass

class RegistroNoEncontradoError(ErrorGestionEventos):
    """Se lanza cuando no se encuentra un registro de asistencia."""
    pass

class EstadoInvalidoError(ErrorGestionEventos):
    """Se lanza cuando se intenta asignar un estado inválido."""
    pass
