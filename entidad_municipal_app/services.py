"""
Servicios para la gestión de eventos municipales y registros de asistencia.
Implementa la lógica de negocio relacionada con inscripciones y cancelaciones.
"""

from django.db import transaction
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from typing import Optional, Tuple
from .models.evento_municipal import EventoMunicipal
from .models.registro_asistencia import RegistroAsistencia

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

        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[registro.ciudadano.correo_electronico],
                fail_silently=False
            )
        except Exception as e:
            # Log the error but don't stop the process
            print(f"Error al enviar notificación: {str(e)}")

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
        if not evento.esta_disponible_para_inscripcion():
            raise ErrorGestionEventos(
                "El evento no está disponible para inscripciones"
            )

    def _validar_inscripcion_unica(self, evento: EventoMunicipal, ciudadano) -> None:
        """
        Valida que el ciudadano no tenga una inscripción activa en el evento
        
        Args:
            evento: Instancia del evento
            ciudadano: Instancia del ciudadano
            
        Raises:
            ErrorGestionEventos: Si ya existe una inscripción activa
        """
        if RegistroAsistencia.objects.tiene_inscripcion_activa(evento, ciudadano):
            raise ErrorGestionEventos(
                "Ya tienes una inscripción activa para este evento"
            )

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
            # Obtener y bloquear el evento para operaciones concurrentes
            evento = EventoMunicipal.objects.select_for_update().get(pk=evento_id)
            
            # Validar que el ciudadano no tenga una inscripción activa
            self._validar_inscripcion_unica(evento, ciudadano)
            
            # Determinar el estado del registro
            if evento.esta_disponible_para_inscripcion() and evento.reducir_cupo_disponible():
                estado = RegistroAsistencia.ESTADO_INSCRITO
            else:
                estado = RegistroAsistencia.ESTADO_EN_ESPERA
            
            # Crear el registro
            registro = RegistroAsistencia.objects.create(
                ciudadano=ciudadano,
                evento=evento,
                estado_registro=estado
            )
            
            # Enviar notificación
            self.servicio_notificaciones.enviar_notificacion_inscripcion(registro)
            
            return registro
            
        except EventoMunicipal.DoesNotExist:
            raise ErrorGestionEventos("El evento especificado no existe")
        except Exception as e:
            raise ErrorGestionEventos(f"Error al procesar la inscripción: {str(e)}")

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
            registro = RegistroAsistencia.objects.select_related('evento').get(pk=registro_id)
            
            if registro.estado_registro == RegistroAsistencia.ESTADO_CANCELADO:
                raise ErrorGestionEventos("El registro ya está cancelado")
            
            # Guardar estado original antes de cancelar
            estado_original = registro.estado_registro
            
            # Cancelar el registro actual
            registro.estado_registro = RegistroAsistencia.ESTADO_CANCELADO
            registro.save()
            
            if estado_original == RegistroAsistencia.ESTADO_INSCRITO:
                registro.evento.aumentar_cupo_disponible()
            
            registro_promovido = None
            if estado_original == RegistroAsistencia.ESTADO_INSCRITO:
                registro_promovido = self._promover_siguiente_en_espera(registro.evento)
            
            # Enviar notificaciones
            self.servicio_notificaciones.enviar_notificacion_inscripcion(registro)
            if registro_promovido:
                self.servicio_notificaciones.enviar_notificacion_inscripcion(registro_promovido)
            
            return registro, registro_promovido
            
        except RegistroAsistencia.DoesNotExist:
            raise ErrorGestionEventos("El registro especificado no existe")
        except Exception as e:
            raise ErrorGestionEventos(f"Error al procesar la cancelación: {str(e)}")

    def _promover_siguiente_en_espera(self, evento: EventoMunicipal) -> Optional[RegistroAsistencia]:
        """
        Promueve al siguiente ciudadano en la lista de espera
        
        Args:
            evento: Instancia del evento
            
        Returns:
            Optional[RegistroAsistencia]: Registro promovido si existe
        """
        siguiente = RegistroAsistencia.objects.obtener_siguiente_en_espera(evento)
        if siguiente:
            siguiente.estado_registro = RegistroAsistencia.ESTADO_INSCRITO
            siguiente.save()
            return siguiente
        return None
