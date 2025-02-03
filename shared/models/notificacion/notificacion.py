from django.db import models
from django.utils import timezone
from ciudadano_app.models import Ciudadano

class Notificacion(models.Model):
    ciudadano = models.ForeignKey(
        'ciudadano_app.Ciudadano',
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    mensaje = models.TextField()
    fecha = models.DateTimeField(default=timezone.now)
    leida = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha']

    def _str_(self):
        return f"Notificación para {self.ciudadano.nombre_completo}: {self.mensaje[:50]}..."