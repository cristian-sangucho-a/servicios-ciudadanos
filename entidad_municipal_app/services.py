"""
Servicios para la gestión de eventos municipales y registros de asistencia.
Implementa la lógica de negocio relacionada con inscripciones y cancelaciones.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from typing import Optional, Tuple
from .models import EventoMunicipal, RegistroAsistencia

class ErrorGestionEventos(Exception):
    """Excepción personalizada para errores en la gestión de eventos"""
    pass

class ServicioNotificaciones:
    """Servicio para el envío de notificaciones relacionadas con eventos"""
    
    @staticmethod
    def enviar_notificacion_inscripcion(registro: RegistroAsistencia) -> None:
        """
        Envía una notificación por correo sobre el estado de la inscripción
        
        Args:
            registro: Instancia de RegistroAsistencia con la información de la inscripción
        """
        plantillas_mensajes = {
            RegistroAsistencia.ESTADO_INSCRITO: "Tu inscripción ha sido confirmada",
            RegistroAsistencia.ESTADO_EN_ESPERA: "Has sido agregado a la lista de espera",
            RegistroAsistencia.ESTADO_CANCELADO: "Tu inscripción ha sido cancelada",
        }

        mensaje_estado = plantillas_mensajes.get(
            registro.estado_registro,
            "Ha habido una actualización en tu registro"
        )

        asunto = f'Actualización de registro - {registro.evento.nombre_evento}'
        mensaje = f'''
        Hola {registro.ciudadano.obtener_nombre_completo()},

        {mensaje_estado} para el evento "{registro.evento.nombre_evento}".
        
        Detalles del evento:
        - Fecha: {registro.evento.obtener_formato_fecha()}
        - Lugar: {registro.evento.lugar_evento}
        - Estado de tu registro: {registro.estado_registro}
        
        Gracias por tu interés en nuestros eventos municipales.
        '''
        
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[registro.ciudadano.obtener_correo_electronico()],
            fail_silently=False,
        )

class GestorRegistroAsistencia:
    """Gestiona las operaciones relacionadas con registros de asistencia a eventos"""

    def __init__(self):
        self.servicio_notificaciones = ServicioNotificaciones()

    def _validar_evento_disponible(self, evento: EventoMunicipal) -> None:
        """
        Valida que el evento esté disponible para inscripciones
        
        Args:
            evento: Instancia del evento a validar
            
        Raises:
            ErrorGestionEventos: Si el evento no está disponible
        """
        if not evento.verificar_estado_permite_inscripciones():
            raise ErrorGestionEventos("El evento no está abierto para inscripciones")

    def _validar_inscripcion_unica(self, evento: EventoMunicipal, ciudadano) -> None:
        """
        Valida que el ciudadano no tenga una inscripción activa en el evento
        
        Args:
            evento: Instancia del evento
            ciudadano: Instancia del ciudadano
            
        Raises:
            ErrorGestionEventos: Si ya existe una inscripción activa
        """
        inscripcion_existente = RegistroAsistencia.objects.filter(
            ciudadano=ciudadano,
            evento=evento,
            estado_registro__in=[
                RegistroAsistencia.ESTADO_INSCRITO,
                RegistroAsistencia.ESTADO_EN_ESPERA
            ]
        ).exists()

        if inscripcion_existente:
            raise ErrorGestionEventos("Ya tienes una inscripción activa para este evento")

    @transaction.atomic
    def procesar_solicitud_inscripcion(self, evento_id: int, ciudadano) -> RegistroAsistencia:
        """
        Procesa una solicitud de inscripción a un evento
        
        Args:
            evento_id: ID del evento
            ciudadano: Instancia del ciudadano
            
        Returns:
            RegistroAsistencia: Registro creado
            
        Raises:
            ErrorGestionEventos: Si hay problemas con la inscripción
        """
        try:
            evento = EventoMunicipal.objects.select_for_update().get(id=evento_id)
        except EventoMunicipal.DoesNotExist:
            raise ErrorGestionEventos("El evento especificado no existe")

        self._validar_evento_disponible(evento)
        self._validar_inscripcion_unica(evento, ciudadano)

        estado_registro = (RegistroAsistencia.ESTADO_INSCRITO 
                         if evento.verificar_disponibilidad_cupos() 
                         else RegistroAsistencia.ESTADO_EN_ESPERA)

        registro = RegistroAsistencia.objects.create(
            ciudadano=ciudadano,
            evento=evento,
            estado_registro=estado_registro
        )

        if estado_registro == RegistroAsistencia.ESTADO_INSCRITO:
            evento.reducir_cupo_disponible()

        self.servicio_notificaciones.enviar_notificacion_inscripcion(registro)
        
        return registro

    @transaction.atomic
    def procesar_cancelacion_inscripcion(self, registro_id: int) -> Tuple[RegistroAsistencia, Optional[RegistroAsistencia]]:
        """
        Procesa la cancelación de una inscripción y maneja la lista de espera
        
        Args:
            registro_id: ID del registro a cancelar
            
        Returns:
            tuple: (registro_cancelado, registro_promovido)
            
        Raises:
            ErrorGestionEventos: Si hay problemas con la cancelación
        """
        try:
            registro = RegistroAsistencia.objects.select_for_update().get(id=registro_id)
        except RegistroAsistencia.DoesNotExist:
            raise ErrorGestionEventos("El registro de asistencia no existe")

        if not registro.verificar_estado_activo():
            raise ErrorGestionEventos("Solo se pueden cancelar inscripciones activas")

        # Guardar estado original antes de la cancelación
        estado_original = registro.estado_registro

        # Cancelar la inscripción actual
        registro.actualizar_estado(RegistroAsistencia.ESTADO_CANCELADO)
        self.servicio_notificaciones.enviar_notificacion_inscripcion(registro)

        registro_promovido = None
        # Verificar si el estado original era INSCRITO para promover
        if estado_original == RegistroAsistencia.ESTADO_INSCRITO:
            registro_promovido = self._promover_siguiente_en_espera(registro.evento)
            if not registro_promovido:
                # Si no hay nadie en espera, aumentar el cupo disponible
                registro.evento.aumentar_cupo_disponible()

        return registro, registro_promovido

    def _promover_siguiente_en_espera(self, evento: EventoMunicipal) -> Optional[RegistroAsistencia]:
        """
        Promueve al siguiente ciudadano en la lista de espera
        
        Args:
            evento: Instancia del evento
            
        Returns:
            Optional[RegistroAsistencia]: Registro promovido si existe
        """
        siguiente_en_espera = RegistroAsistencia.objects.filter(
            evento=evento,
            estado_registro=RegistroAsistencia.ESTADO_EN_ESPERA
        ).order_by('fecha_inscripcion').first()

        if siguiente_en_espera:
            siguiente_en_espera.actualizar_estado(RegistroAsistencia.ESTADO_INSCRITO)
            self.servicio_notificaciones.enviar_notificacion_inscripcion(siguiente_en_espera)
            return siguiente_en_espera
        
        return None
