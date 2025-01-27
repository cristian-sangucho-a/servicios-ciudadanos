from ciudadano_app.models.Reporte import Reporte
from ciudadano_app.models.RepositorioDeReporte import RepositorioDeReporte

class ServicioDeReporte():
    def __init__(self, reporte_repositorio: RepositorioDeReporte):
        self.reporte_repositorio = reporte_repositorio

    # De acuerdo a la escala fiboncacci: 1, 1, 2, 3, 5, 8, 13
    def __obtener_prioridad(self, cantidad_reportes):
        if cantidad_reportes >= 13:
            return 1
        if cantidad_reportes >= 8:
            return 2
        if cantidad_reportes >= 5:
            return 3
        if cantidad_reportes >= 3:
            return 4
        if cantidad_reportes >= 0:
            return 5

    def priorizar(self, reporte: Reporte):
        reportes_previos = self.reporte_repositorio.obtener_reportes_por_asunto(reporte.tipo_reporte.asunto) or []
        cantidad_reportes = len(reportes_previos)

        reporte.prioridad = self.__obtener_prioridad(cantidad_reportes)

        self.reporte_repositorio.actualziar_prioridad_de_reporte_por_asunto(reporte.tipo_reporte.asunto, reporte.prioridad)

        return reporte

    def enviar_reporte(self, reporte: Reporte):
        if not reporte.validar_reporte():
            raise ValueError("El reporte no es válido.")
        self.reporte_repositorio.agregar_reporte(reporte)