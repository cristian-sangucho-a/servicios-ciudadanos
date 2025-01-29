from django.db import models

from ciudadano_app.models.reporte.reporte import Reporte

class ReporteMunicipal(models.Model):
    """
    Modelo que representa un reporte municipal.

    Atributos:
        reporte_ciudadano (ForeignKey): Relación con el reporte ciudadano original.
        estado (CharField): Estado del reporte.
        evidencia (TextField): Evidencia opcional de la solución.
    """
    id = models.AutoField(primary_key=True)
    reporte_ciudadano = models.ForeignKey(
        Reporte, on_delete=models.CASCADE
    )
    estado = models.CharField(max_length=50, default="no_asignado")
    evidencia = models.TextField(blank=True, null=True)

    def __str__(self):
        """
        Retorna una representación en cadena del reporte municipal.
        """
        return f"Reporte {self.id}: {self.estado}"

    def obtener_estado(self):
        """
        Devuelve el estado actual del reporte.

        :return: Estado del reporte.
        :rtype: str
        """
        return self.estado

    def registrar_evidencia(self, descripcion_evidencia):
        """
        Registra evidencia en el reporte municipal.

        :param descripcion_evidencia: Descripción de la evidencia.
        :type descripcion_evidencia: str
        """
        self.evidencia = descripcion_evidencia
        self.estado = "resuelto"
        self.save()

    def obtener_evidencia(self):
        """
        Devuelve la evidencia registrada en el reporte.

        :return: Evidencia del reporte.
        :rtype: str
        """
        return self.evidencia if self.evidencia else ""


    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado del reporte municipal y lo guarda en la base de datos.

        :param nuevo_estado: Nuevo estado a asignar al reporte.
        :type nuevo_estado: str
        :raises ValueError: Si el estado proporcionado no es válido.
        """
        ESTADOS_VALIDOS = ["asignado", "atendiendo", "resuelto", "postergado"]

        if nuevo_estado not in ESTADOS_VALIDOS:
            raise ValueError(f"Estado '{nuevo_estado}' no es válido. Estados permitidos: {ESTADOS_VALIDOS}")

        self.estado = nuevo_estado
        self.save()