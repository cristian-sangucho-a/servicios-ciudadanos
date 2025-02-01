from django.db import models
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

class Notificacion(models.Model):
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, related_name="notificaciones")
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificación para {self.ciudadano.nombre_completo}: {self.titulo}"