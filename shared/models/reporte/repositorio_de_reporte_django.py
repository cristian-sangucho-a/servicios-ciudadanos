from shared.models import Reporte, TipoReporte
from ciudadano_app.models import Ciudadano
from .repositorio_de_reporte import RepositorioDeReporte


class RepositorioDeReporteDjango(RepositorioDeReporte):
    def __init__(self):
        """
        Constructor de la clase, puede utilizarse para inicializar conexiones a la base de datos
        o configuraciones específicas si es necesario.
        """
        pass

    def obtener_reportes_por_asunto(self, asunto: str):
        """
        Implementación del método para obtener reportes por asunto utilizando el ORM de Django.

        Args:
            asunto (str): El asunto del reporte basado en el cual se filtran los reportes.

        Returns:
            list[Reporte]: Una lista de instancias de Reporte que coinciden con el asunto proporcionado.
        """
        return list(Reporte.objects.filter(tipo_reporte__asunto=asunto))

    def agregar_reporte(self, reporte: Reporte):
        """
        Implementación del método para agregar un reporte a la base de datos.

        Args:
            reporte (Reporte): La instancia de Reporte a guardar en la base de datos.
        """
        reporte.save()

    def actualizar_prioridad_de_reporte_por_asunto(self, asunto: str, prioridad: int):
        """
        Implementación del método para actualizar la prioridad de los reportes por asunto.

        Args:
            asunto (str): El asunto de los reportes cuya prioridad se desea actualizar.
            prioridad (int): El nuevo valor de prioridad para los reportes.
        """
        Reporte.objects.filter(tipo_reporte__asunto=asunto).update(prioridad=prioridad)

    def obtener_reportes_ordenados_prioridad(self):
        return list(Reporte.objects.order_by('-prioridad'))
