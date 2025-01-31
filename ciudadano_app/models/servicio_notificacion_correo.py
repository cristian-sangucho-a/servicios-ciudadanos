from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from ciudadano_app.models.reserva.reserva import Reserva

class ServicioNotificacionPorCorreo():

    def enviar_invitacion(self, reserva: Reserva):
        for email in reserva.correos_invitados.split(","):
            msg = EmailMultiAlternatives(
                'Invitación a actividad privada en espacio comunal',
                'Hola, se ha enviado una solicitud para que asistas a una actividad en el espacio comunal en la fecha '
                + str(reserva.fecha_reserva)
                + ' a las '
                + str(reserva.hora_inicio)
                + ' hasta las '
                + str(reserva.hora_fin)
                + 'en el area comunal'
                + str(reserva.area_comunal),
                settings.EMAIL_HOST_USER,
                [email]
            )
            try:
                msg.send()
            except:
                # TODO: manejar el error enviandole a la vista
                return False

        return True

    def enviar_cancelacion(self, reserva: Reserva):
        for email in reserva.correos_invitados.split(","):
            msg = EmailMultiAlternatives(
                'Invitación a actividad privada en espacio comunal',
                'Hola, se ha cancelado una reserva a la que hacias parte. '
                + str(reserva.area_comunal),
                settings.EMAIL_HOST_USER,
                [email]
            )
            try:
                msg.send()
            except:
                # TODO: manejar el error enviandole a la vista
                return False
        return True