from .reporte import Reporte
from .repositorio_de_reporte import RepositorioDeReporte
from collections import OrderedDict

prioridades: dict[str, dict[str, int]] = {
    "cantidad_prioridad_1": {"recurrencia": 13, "prioridad": 1},
    "cantidad_prioridad_2": {"recurrencia": 8, "prioridad": 2},
    "cantidad_prioridad_3": {"recurrencia": 5, "prioridad": 3},
    "cantidad_prioridad_4": {"recurrencia": 3, "prioridad": 4},
    "cantidad_prioridad_5": {"recurrencia": 0, "prioridad": 5},
}


class ServicioDeReporte:
    def __init__(self, reporte_repositorio: RepositorioDeReporte):
        """
        Inicializa el ServicioDeReporte con un repositorio de reportes.

        Args:
            reporte_repositorio (RepositorioDeReporte): Un objeto repositorio que implementa la interfaz
            para operaciones CRUD sobre reportes.
        """
        self.reporte_repositorio = reporte_repositorio

    def __obtener_prioridad(self, cantidad_reportes):
        """
        Determina la prioridad del reporte según la cantidad de reportes previos similares,
        utilizando la escala de Fibonacci: 1, 1, 2, 3, 5, 8, 13.

        Args:
            cantidad_reportes (int): Número de reportes previos con el mismo asunto.

        Returns:
            int: Nivel de prioridad asignado al reporte.
        """
        
        for prioridad in prioridades:
            if cantidad_reportes >= prioridades[prioridad]["recurrencia"]:
                return prioridades[prioridad]["prioridad"]
            
    def priorizar(self, reporte: Reporte):
        """
        Asigna una prioridad a un reporte basado en la cantidad de reportes previos con el mismo asunto.

        Args:
            reporte (Reporte): El reporte a priorizar.

        Returns:
            Reporte: El reporte con su prioridad actualizada.
        """
        reportes_previos = (
            self.reporte_repositorio.obtener_reportes_por_asunto(
                reporte.tipo_reporte.asunto
            )
            or []
        )
        cantidad_reportes = len(reportes_previos)
        reporte.prioridad = self.__obtener_prioridad(cantidad_reportes)
        self.reporte_repositorio.actualizar_prioridad_de_reporte_por_asunto(
            reporte.tipo_reporte.asunto, reporte.prioridad
        )
        return reporte

    def enviar_reporte(self, reporte: Reporte):
        """
        Valida y envía un reporte al repositorio para ser agregado a la base de datos.

        Args:
            reporte (Reporte): El reporte a enviar.

        Raises:
            ValueError: Si el reporte no es válido.
        """
        if not reporte.validar_reporte():
            raise ValueError("El reporte no es válido.")
        self.reporte_repositorio.agregar_reporte(reporte)

        return reporte
    
    def obetener_lista_reportes_por_asunto(self):
        reportes = Reporte.objects.all().order_by('tipo_reporte__asunto', '-prioridad')
    
        grouped_reportes = {}
        for reporte in reportes:
            asunto = reporte.tipo_reporte.asunto
            if asunto not in grouped_reportes:
                grouped_reportes[asunto] = []
            grouped_reportes[asunto].append(reporte)
        
        # Sort the grouped_reportes by the prioridad of the first reporte in each group (descending order)
        sorted_grouped_reportes = OrderedDict(
            sorted(grouped_reportes.items(), key=lambda item: item[1][0].prioridad or 0)
        )
        
        return sorted_grouped_reportes
