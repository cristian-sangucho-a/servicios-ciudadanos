from django.db import models

from ciudadano_app.models import Ciudadano
from ciudadano_app.models.TipoReporte import TipoReporte

class Reporte(models.Model):
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE)
    tipo_reporte = models.ForeignKey(TipoReporte, on_delete=models.CASCADE)
    ubicacion = models.CharField(max_length=255)
    prioridad = models.IntegerField(default=None, null=True, blank=True)

    def validar_reporte(self):
        return bool(self.ciudadano and self.tipo_reporte and self.ubicacion)

    def __str__(self):
        return f"Reporte de {self.tipo_reporte.asunto} por {self.ciudadano.nombre}"