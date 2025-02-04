from django.db import models

class Departamento(models.Model):
    """Modelo que representa un departamento municipal en el sistema.

    Attributes:
        nombre (CharField): Nombre único del departamento.
        descripcion (TextField): Breve descripción del departamento.
    """

    nombre = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="Nombre del Departamento",
        help_text="Nombre único del departamento"
    )

    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Breve descripción del departamento"
    )

    def __str__(self) -> str:
        """Retorna una representación en cadena del departamento.

        Returns:
            str: Nombre del departamento.
        """
        return self.nombre
