from django.db import models
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

class Notificacion(models.Model):
    ciudadano = models.ForeignKey(
        Ciudadano,
        on_delete=models.CASCADE,
        verbose_name="Ciudadano",
        help_text="El ciudadano al que se le envía la notificación"
    )
    mensaje = models.TextField(
        verbose_name="Mensaje",
        help_text="El contenido del mensaje de la notificación"
    )
    fecha = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de la Notificación",
        help_text="Fecha y hora en que se registró la notificación"
    )

    class Meta:
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"
        ordering = ["-fecha"]

    def __str__(self):
        return f"Notificación a {self.ciudadano} en {self.fecha}"
