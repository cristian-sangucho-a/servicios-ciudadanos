from django.db import models
from ciudadano_app.models import Ciudadano, AreaComunal


class Reserva(models.Model):
    """
    Modelo que representa una reserva realizada por un ciudadano en un área comunal.

    Attributes:
        fecha_reserva (DateField): La fecha de la reserva.
        hora_inicio (TimeField): La hora de inicio de la reserva.
        hora_fin (TimeField): La hora de fin de la reserva.
        tipo_reserva (CharField): El tipo de reserva ("pública" o "privada").
        correos_invitados (CharField): Los correos electrónicos de los invitados separados por comas.
        estado_reserva (CharField): El estado actual de la reserva ("Activa", "Cancelada", etc.).
        ciudadano (ForeignKey): Relación con el ciudadano que realizó la reserva.
        area_comunal (ForeignKey): Relación con el área comunal reservada.

    Methods:
        obtener_id: Retorna el ID de la reserva.
        agregar_correos_invitados: Agrega correos de invitados a una reserva privada.
        obtener_area_comunal: Retorna el área comunal asociada a la reserva.
        obtener_correos_invitados: Retorna los correos de los invitados de la reserva.
    """

    fecha_reserva = models.DateField(
        help_text="Fecha de la reserva"
    )
    hora_inicio = models.TimeField(
        help_text="Hora de inicio de la reserva"
    )
    hora_fin = models.TimeField(
        help_text="Hora de fin de la reserva"
    )
    tipo_reserva = models.CharField(
        max_length=50,
        help_text="Tipo de reserva",
    )
    correos_invitados = models.CharField(
        max_length=100,
        help_text="Correos de los invitados",
        default=""
    )
    estado_reserva = models.CharField(
        max_length=50,
        help_text="Estado de la reserva",
        default="Activa"
    )
    ciudadano = models.ForeignKey(
        Ciudadano, on_delete=models.CASCADE,
        related_name='reservas'
    )
    area_comunal = models.ForeignKey(  # Cambiado de OneToOneField a ForeignKey
        AreaComunal,
        on_delete=models.CASCADE,
        related_name='reservas'
    )

    def obtener_id(self):
        """
        Retorna el ID de la reserva.

        Returns:
            int: El ID de la reserva.
        """
        return self.pk

    def agregar_correos_invitados(self, correos_invitados):
        """
        Agrega correos de invitados a una reserva privada.

        Args:
            correos_invitados (str): Los correos de los invitados separados por comas.

        Steps:
            - Verifica si la reserva es pública. Si lo es, lanza una excepción.
            - Actualiza el campo `correos_invitados` con los nuevos correos.

        Returns:
            bool: True si los correos se agregaron correctamente, False si ocurrió un error.

        Raises:
            ValueError: Si se intenta agregar invitados a una reserva pública.
        """
        try:
            if self.tipo_reserva == "publica":
                raise ValueError("No se pueden agregar invitados a una reserva pública")
            self.correos_invitados = correos_invitados
        except Exception:
            return False
        return True

    def obtener_area_comunal(self):
        """
        Retorna el área comunal asociada a la reserva.

        Returns:
            AreaComunal: El área comunal asociada a la reserva.
        """
        return self.area_comunal

    def obtener_correos_invitados(self):
        """
        Retorna los correos de los invitados de la reserva.

        Returns:
            str: Los correos de los invitados separados por comas.
        """
        return self.correos_invitados