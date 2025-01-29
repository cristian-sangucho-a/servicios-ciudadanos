from django.db import models

from ciudadano_app.models.reporte.reporte import Reporte


class Reporte(models.Model):
    """
    Modelo que representa un reporte en el sistema.

    Atributos:
        descripcion_problema (TextField): Descripción detallada del problema reportado.
        estado (CharField): Estado actual del reporte (por defecto, 'no_asignado').
        evidencia (TextField, opcional): Evidencia asociada al reporte.
        indice_prioridad (IntegerField): Índice de prioridad calculado en base a palabras clave.
    """
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE)
    descripcion_problema = models.TextField()
    estado = models.CharField(max_length=50, default="no_asignado")
    evidencia = models.TextField(blank=True, null=True)
    indice_prioridad = models.IntegerField(default=0)

    def __str__(self):
        """
        Devuelve una representación en cadena del objeto.

        :return: Descripción del problema con su estado.
        :rtype: str
        """
        return f"Reporte: {self.descripcion_problema[:50]}... (Estado: {self.estado})"

    def cambiar_estado(self, nuevo_estado):
        """
        Cambia el estado del reporte.

        :param nuevo_estado: Nuevo estado del reporte.
        :type nuevo_estado: str
        """
        self.estado = nuevo_estado
        self.save()

    def registrar_evidencia(self, nueva_evidencia):
        """
        Registra la evidencia asociada al reporte.

        :param nueva_evidencia: Evidencia en formato texto.
        :type nueva_evidencia: str
        """
        self.evidencia = nueva_evidencia
        self.save()

    def establecer_indice_prioridad(self, keywords):
        """
        Calcula la prioridad del reporte en base a palabras clave definidas por el departamento.

        :param keywords: Diccionario con palabras clave para cada categoría de prioridad.
        :type keywords: dict
        """
        indice_impacto_seguridad = self.__calcular_indice(
            keywords.get('impacto_seguridad', {})
        )
        indice_afectacion_publica = self.__calcular_indice(
            keywords.get('afectacion_publica', {})
        )
        indice_posibilidad_agravamiento = self.__calcular_indice(
            keywords.get('posibilidad_agravamiento', {})
        )

        self.indice_prioridad = (
                indice_impacto_seguridad * 0.5 +
                indice_afectacion_publica * 0.3 +
                indice_posibilidad_agravamiento * 0.2
        )
        self.save()

    def __calcular_indice(self, keywords_dict):
        """
        Calcula el índice basado en palabras clave y su impacto.

        :param descripcion: Descripción del problema.
        :type descripcion: str
        :param keywords_dict: Diccionario con niveles de palabras clave.
        :type keywords_dict: dict
        :return: Valor del índice (1-3).
        :rtype: int
        """
        descripcion_lower = self.descripcion_problema.lower()

        if any(palabra in descripcion_lower for palabra in keywords_dict.get('alto', [])):
            return 3
        if any(palabra in descripcion_lower for palabra in keywords_dict.get('medio', [])):
            return 2
        return 1
