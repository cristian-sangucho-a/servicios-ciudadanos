from django.db import models

class Sugerencia(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    estado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    @classmethod
    def crear_sugerencia_canal(cls, nombre, descripcion):
        sugerencia = Sugerencia.objects.create(
            nombre=nombre,
            descripcion=descripcion
        )
        return sugerencia

    @staticmethod
    def obtener_sugerencias():
        return Sugerencia.objects.all()