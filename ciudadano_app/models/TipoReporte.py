from django.db import models

class TipoReporte(models.Model):
    asunto = models.CharField(max_length=200)
    descripcion = models.TextField()

    def __str__(self):
        return self.asunto
