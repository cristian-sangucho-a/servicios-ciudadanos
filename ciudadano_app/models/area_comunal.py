from django.db import models

class AreaComunal(models.Model):
    nombre_area = models.CharField(
        max_length=100,
        help_text="Nombre del área comunal",
        default="Área Comunal"
    )
    pass