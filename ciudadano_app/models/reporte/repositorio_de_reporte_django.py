from ciudadano_app.models import Ciudadano, Reporte, TipoReporte
from ciudadano_app.models.reporte.repositorio_de_reporte import RepositorioDeReporte


class RepositorioDeReporteDjango(RepositorioDeReporte):
    def _init_(self):
        pass

    def obtener_reportes_por_asunto(self, asunto: str):
        return list(Reporte.objects.filter(tipo_reporte__asunto=asunto))

    def agregar_reporte(self, reporte: Reporte):
        reporte.save()

    def actualizar_prioridad_de_reporte_por_asunto(self, asunto: str, prioridad: int):
        Reporte.objects.filter(tipo_reporte__asunto=asunto).update(prioridad=prioridad)
