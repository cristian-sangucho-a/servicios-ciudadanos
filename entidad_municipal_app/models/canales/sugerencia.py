from django.db import models

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal


class Sugerencia(models.Model):
    ESTADOS_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
    ]
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, related_name="sugerencias")
    entidad_municipal = models.ForeignKey(EntidadMunicipal, on_delete=models.CASCADE, related_name="sugerencias")
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    canal_creado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='Pendiente')
    @classmethod
    def crear_sugerencia_canal(cls, nombre, descripcion, ciudadano, entidad_municipal):
        sugerencia = Sugerencia.objects.create(
            ciudadano=ciudadano,
            entidad_municipal=entidad_municipal,
            nombre=nombre,
            descripcion=descripcion
        )
        return sugerencia

    @staticmethod
    def obtener_sugerencias():
        return Sugerencia.objects.all()