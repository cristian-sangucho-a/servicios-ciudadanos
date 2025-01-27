from django.db import models

class Ciudadano(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    identificacion = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} - {self.identificacion}"