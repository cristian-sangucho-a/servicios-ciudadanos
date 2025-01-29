from django.db import models

from entidad_municipal_app.models.departamento.departamento import Departamento


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

    #Campo para el departamento al cual se asigna el reporte
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)

    # Campo para la prioridad de atención del reporte dependiendo del asunto que tenga
    prioridad_de_atencion = models.IntegerField(default=0)
    def __str__(self):
        """
        Devuelve el asunto del tipo de reporte como su representación en cadena, facilitando la identificación en interfaces de usuario.

        Returns:
            str: Asunto del tipo de reporte.
        """
        return self.asunto
