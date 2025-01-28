from django.db import models
from ciudadano_app.models import Ciudadano


class Reserva(models.Model):
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
        help_text="Tipo de reserva"
    )
    correos_invitados = models.CharField(
        max_length=100,
        help_text="Correos de los invitados"
    )
    ciudadano = models.ForeignKey(
        Ciudadano, on_delete=models.CASCADE
    )

    def agregar_correos_invitados(self, correos_invitados):
        try:
            self.correos_invitados = correos_invitados
        except Exception as e:
            return False
        return True

    def obtener_correos_invitados(self):
        return self.correos_invitados