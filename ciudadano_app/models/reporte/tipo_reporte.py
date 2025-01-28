from django.db import models

class TipoReporte(models.Model):
    """
    Modelo que representa un tipo de reporte en el sistema.

    Atributos:
        asunto (CharField): El asunto o título del tipo de reporte, utilizado para identificación rápida.
        descripcion (TextField): Una descripción detallada del tipo de reporte.

    Métodos:
        __str__(self):
            Devuelve una representación en cadena del objeto, utilizando el asunto del tipo de reporte.
    """
    # Campo para el asunto o título del tipo de reporte.
    asunto = models.CharField(max_length=200)

    # Campo para una descripción textual extensa del tipo de reporte.
    descripcion = models.TextField()

    def __str__(self):
        """
        Devuelve el asunto del tipo de reporte como su representación en cadena, facilitando la identificación en interfaces de usuario.

        Returns:
            str: Asunto del tipo de reporte.
        """
        return self.asunto
