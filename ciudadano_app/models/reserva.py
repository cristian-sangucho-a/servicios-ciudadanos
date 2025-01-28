from django.db import models
from ciudadano_app.models import Ciudadano, AreaComunal


class Reserva(models.Model):
    fecha_reserva = models.DateField(
        help_text="Fecha de la reserva",
        null=True
    )
    hora_inicio = models.TimeField(
        help_text="Hora de inicio de la reserva",
        null=True
    )
    hora_fin = models.TimeField(
        help_text="Hora de fin de la reserva",
        null=True
    )
    tipo_reserva = models.CharField(
        max_length=50,
        help_text="Tipo de reserva",
        null=True
    )
    correos_invitados = models.CharField(
        max_length=100,
        help_text="Correos de los invitados",
        default=""
    )
    ciudadano = models.ForeignKey(
        Ciudadano, on_delete=models.CASCADE,
        null=True
    )
    area_comunal = models.OneToOneField(
        AreaComunal,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='+',
        default=1)

    def obtener_id(self):
        return self.pk

    def agregar_correos_invitados(self, correos_invitados):
        try:
            self.correos_invitados = correos_invitados
        except Exception as e:
            return False
        return True

    def obtener_area_comunal(self):
        return self.area_comunal

    def obtener_correos_invitados(self):
        return self.correos_invitados
