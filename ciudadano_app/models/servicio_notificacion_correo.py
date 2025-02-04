from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from ciudadano_app.models.reserva.reserva import Reserva


class ServicioNotificacionPorCorreo:
    """
    Clase que maneja el envío de notificaciones por correo electrónico relacionadas con reservas.

    Attributes:
        No tiene atributos específicos.
    """

    def enviar_invitacion(self, reserva: Reserva) -> bool:
        """
        Envía una invitación por correo electrónico a los invitados de una reserva.

        Args:
            reserva (Reserva): La reserva que contiene los detalles de la actividad y los correos de los invitados.

        Steps:
            - Itera sobre los correos de los invitados separados por comas.
            - Crea un mensaje de correo electrónico con los detalles de la reserva.
            - Intenta enviar el correo electrónico a cada invitado.
            - Si ocurre un error al enviar el correo, retorna False.

        Returns:
            bool: True si todos los correos se enviaron correctamente, False si ocurrió un error.

        Raises:
            Exception: Captura cualquier excepción durante el envío del correo, pero no la propaga.
        """
        for email in reserva.correos_invitados.split(","):
            msg = EmailMultiAlternatives(
                'Invitación a actividad privada en espacio comunal',
                'Hola, se ha enviado una solicitud para que asistas a una actividad en el espacio comunal en la fecha '
                + str(reserva.fecha_reserva)
                + ' a las '
                + str(reserva.hora_inicio)
                + ' hasta las '
                + str(reserva.hora_fin)
                + ' en el área comunal '
                + str(reserva.area_comunal),
                settings.EMAIL_HOST_USER,
                [email]  # Elimina espacios en blanco alrededor del correo
            )
            msg.send()
        return True

    def enviar_cancelacion(self, reserva: Reserva) -> bool:
        """
        Envía una notificación de cancelación por correo electrónico a los invitados de una reserva.

        Args:
            reserva (Reserva): La reserva que contiene los detalles de la actividad y los correos de los invitados.

        Steps:
            - Itera sobre los correos de los invitados separados por comas.
            - Crea un mensaje de correo electrónico informando la cancelación de la reserva.
            - Intenta enviar el correo electrónico a cada invitado.
            - Si ocurre un error al enviar el correo, retorna False.

        Returns:
            bool: True si todos los correos se enviaron correctamente, False si ocurrió un error.

        Raises:
            Exception: Captura cualquier excepción durante el envío del correo, pero no la propaga.
        """
        for email in reserva.correos_invitados.split(","):
            msg = EmailMultiAlternatives(
                'Cancelación de reserva en espacio comunal',
                'Hola, se ha cancelado una reserva a la que hacías parte. '
                + 'La reserva era para el área comunal: '
                + str(reserva.area_comunal),
                settings.EMAIL_HOST_USER,
                [email]  # Elimina espacios en blanco alrededor del correo
            )
            msg.send()
        return True