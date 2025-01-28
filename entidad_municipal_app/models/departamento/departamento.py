
class Departamento:
    def __init__(self, nombre):
        self.__nombre = nombre
        self.__reportes = []
        self.__palabras_clave_priorizacion = {
            'impacto_seguridad': {
                'alto': [],
                'medio': []
            },
            'afectacion_publica': {
                'alto': [],
                'medio': []
            },
            'posibilidad_agravamiento': {
                'alto': [],
                'medio': []
            }
        }

    def obtener_nombre(self):
        return self.__nombre

    def agregar_reporte(self, reporte):
        self.__reportes.append(reporte)
        reporte.cambiar_estado("asignado")

    def obtener_reportes_asignados(self):
        return self.__reportes

    def priorizar_reportes(self):
        self.__reportes.sort(key=lambda r: r.obtener_indice_prioridad(), reverse=True)

    def obtener_reporte_por_id(self, id_reporte):
        for reporte in self.__reportes:
            if reporte.obtener_id() == id_reporte:
                return reporte
        return None

    def atender_reporte(self, reporte):
        reporte.cambiar_estado("atendiendo")

    def registrar_evidencia(self, reporte, evidencia):
        reporte.registrar_evidencia(evidencia)

    def postergar_reporte(self, reporte):
        reporte.cambiar_estado("postergado")
