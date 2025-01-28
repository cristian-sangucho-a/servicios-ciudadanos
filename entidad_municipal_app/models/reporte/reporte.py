class Reporte:
    def __init__(self, id_reporte, descripcion_problema):
        self.__id_reporte = id_reporte
        self.__descripcion_problema = descripcion_problema
        self.__estado = "no_asignado"
        self.__evidencia = ""
        self.__indice_prioridad = 0

    def obtener_id(self):
        return self.__id_reporte

    def obtener_estado(self):
        return self.__estado

    def cambiar_estado(self, estado):
        self.__estado = estado

    def obtener_descripcion(self):
        return self.__descripcion_problema

    def registrar_evidencia(self, evidencia):
        self.__evidencia = evidencia

    def obtener_evidencia(self):
        return self.__evidencia

    def obtener_indice_prioridad(self):
        return self.__indice_prioridad

    def establecer_indice_prioridad(self, keywords):
        """
        Calcula la prioridad usando keywords proporcionadas por el departamento

        :param keywords: Diccionario con palabras clave para cada índice
        """
        indice_impacto_seguridad = self.__calcular_indice(
            self.__descripcion_problema,
            keywords.get('impacto_seguridad', {})
        )
        indice_afectacion_publica = self.__calcular_indice(
            self.__descripcion_problema,
            keywords.get('afectacion_publica', {})
        )
        indice_posibilidad_agravamiento = self.__calcular_indice(
            self.__descripcion_problema,
            keywords.get('posibilidad_agravamiento', {})
        )

        self.__indice_prioridad = (
                indice_impacto_seguridad * 0.5 +
                indice_afectacion_publica * 0.3 +
                indice_posibilidad_agravamiento * 0.2
        )

    def __calcular_indice(self, descripcion, keywords_dict):
        """
        Calcula el índice basado en diccionario de keywords

        :param descripcion: Descripción del problema
        :param keywords_dict: Diccionario con niveles de keywords
        :return: Valor del índice (1-3)
        """
        descripcion_lower = descripcion.lower()

        # Verificar palabras clave de alto impacto
        if any(palabra in descripcion_lower for palabra in keywords_dict.get('alto', [])):
            return 3

        # Verificar palabras clave de impacto medio
        if any(palabra in descripcion_lower for palabra in keywords_dict.get('medio', [])):
            return 2

        return 1