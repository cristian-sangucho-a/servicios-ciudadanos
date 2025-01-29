from django.db import models


class Departamento(models.Model):
    """
    Representa un departamento dentro del sistema de gestión de reportes.

    Atributos:
        nombre (CharField): Nombre único del departamento.
    """
    nombre = models.CharField(max_length=20, unique=True)

    def __str__(self):
        """
        Retorna una representación en cadena del departamento.
        """
        return self.nombre

    def atender_reporte_municipal(self, reporte):
        """
        Marca un reporte como 'atendiendo'.

        :param reporte: Instancia de ReporteMunicipal.
        :type reporte: ReporteMunicipal
        """
        reporte.cambiar_estado("atendiendo")
        reporte.save()

    def postergar_reporte(self, reporte):
        """
        Marca un reporte como 'postergado'.

        :param reporte: Instancia de ReporteMunicipal.
        :type reporte: ReporteMunicipal
        """
        reporte.cambiar_estado("postergado")
        reporte.save()

