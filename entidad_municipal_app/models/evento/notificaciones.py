"""
Servicio para el manejo de notificaciones del sistema.
"""
from django.core.mail import send_mail
from django.conf import settings
from entidad_municipal_app.models.evento.enums import EstadoRegistro

class GestorNotificaciones:
    """Gestiona el envío de notificaciones del sistema."""

    PLANTILLAS = {
        EstadoRegistro.INSCRITO.value: {
            'asunto': 'Confirmación de inscripción',
            'mensaje': 'Tu inscripción ha sido confirmada'
        },
        EstadoRegistro.EN_ESPERA.value: {
            'asunto': 'Agregado a lista de espera',
            'mensaje': 'Has sido agregado a la lista de espera'
        },
        EstadoRegistro.CANCELADO.value: {
            'asunto': 'Cancelación de inscripción',
            'mensaje': 'Tu inscripción ha sido cancelada'
        },
    }

    @classmethod
    def enviar_notificacion_inscripcion(cls, registro, evento):
        """
        Envía una notificación por correo sobre el estado de la inscripción.
        """
        plantilla = cls.PLANTILLAS.get(
            registro.estado_registro,
            {
                'asunto': 'Actualización de registro',
                'mensaje': 'Ha habido una actualización en tu registro'
            }
        )

        asunto = f'{plantilla["asunto"]} - {evento.nombre_evento}'
        mensaje = f'''
        Hola {registro.ciudadano.obtener_nombre_completo()},
        
        {plantilla["mensaje"]} para el evento "{evento.nombre_evento}".
        
        Detalles del evento:
        - Fecha: {evento.fecha_realizacion.strftime("%d/%m/%Y %H:%M")}
        - Lugar: {evento.lugar_evento}
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
            print(f"Error al enviar notificación: {str(e)}")
