from django.db import models
from django.core.exceptions import ValidationError
from ciudadano_app.models.reporte.reporte import Reporte


class ReporteMunicipal(models.Model):
    """
    Modelo que representa un reporte municipal derivado de un reporte ciudadano.
    """

    ESTADOS_VALIDOS = [
        "no_asignado",
        "asignado",
        "atendiendo",
        "resuelto",
        "postergado"
    ]

    id = models.AutoField(primary_key=True)
    reporte_ciudadano = models.ForeignKey(
        Reporte,
        on_delete=models.CASCADE,
        verbose_name="Reporte Ciudadano",
        help_text="Reporte ciudadano original"
    )
    estado = models.CharField(
        max_length=50,
        default="no_asignado",
        verbose_name="Estado",
        help_text="Estado actual del reporte municipal"
    )
    evidencia = models.TextField(
        blank=True,
        null=True,
        verbose_name="Evidencia",
        help_text="Evidencia de la atención o resolución del reporte"
    )

    class Meta:
        verbose_name = "Reporte Municipal"
        verbose_name_plural = "Reportes Municipales"
        ordering = ['-id']

    def cambiar_estado(self, nuevo_estado: str):
        """
        Cambia el estado del reporte municipal validando que sea un estado válido.

        Args:
            nuevo_estado (str): Nuevo estado a establecer

        Raises:
            ValidationError: Si el estado no es válido
        """
        if nuevo_estado not in self.ESTADOS_VALIDOS:
            raise ValidationError(
                f"Estado '{nuevo_estado}' no válido. Estados permitidos: {self.ESTADOS_VALIDOS}"
            )
        self.estado = nuevo_estado

    def registrar_evidencia(self, descripcion_evidencia: str):
        """
        Registra evidencia en el reporte y lo marca como resuelto.

        Args:
            descripcion_evidencia (str): Descripción de la evidencia
        """
        self.evidencia = descripcion_evidencia
        self.estado = "resuelto"

    def obtener_departamento(self):
        return self.reporte_ciudadano.tipo_reporte.departamento

    def obtener_prioridad (self):
        return self.reporte_ciudadano.tipo_reporte.prioridad_de_atencion

    def obtener_estado (self):
        return self.estado

    def obtener_evidencia(self):
        return self.evidencia

    def obtener_id(self):
        return self.id

    def __str__(self):
        """
        Representación en cadena del reporte municipal.
        """
        return f"Reporte Municipal {self.id}: {self.estado}"