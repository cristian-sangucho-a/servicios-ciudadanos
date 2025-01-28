from faker.proxy import Faker

from ciudadano_app.models import Ciudadano
from ciudadano_app.models.reporte.reporte import Reporte
from ciudadano_app.models.reporte.repositorio_de_reporte import RepositorioDeReporte
from ciudadano_app.models.reporte.tipo_reporte import TipoReporte


class RepositorioDeReporteEnMemoria(RepositorioDeReporte):
    """
    Una implementación de repositorio que almacena reportes en memoria.

    Utiliza un diccionario para simular una base de datos en memoria,
    con el asunto del reporte como clave y una lista de reportes como valor.
    """

    def __init__(self):
        # Inicializa el diccionario que actuará como base de datos en memoria.
        self.baseDeDato = {}

    def obtener_reportes_por_asunto(self, asunto: str):
        """
        Recupera todos los reportes que coincidan con un asunto específico.

        Args:
            asunto (str): El asunto para filtrar los reportes.

        Returns:
            list: Lista de reportes con el asunto especificado.
        """
        return self.baseDeDato.get(asunto, [])

    def agregar_reporte(self, reporte: Reporte):
        """
        Agrega un nuevo reporte al repositorio en memoria.

        Args:
            reporte (Reporte): El reporte a agregar.
        """
        if reporte.tipo_reporte.asunto not in self.baseDeDato:
            self.baseDeDato[reporte.tipo_reporte.asunto] = []
        self.baseDeDato[reporte.tipo_reporte.asunto].append(reporte)

    def actualizar_prioridad_de_reporte_por_asunto(self, asunto: str, prioridad: int):
        """
        Actualiza la prioridad de todos los reportes para un asunto dado.

        Args:
            asunto (str): El asunto de los reportes a actualizar.
            prioridad (int): La nueva prioridad a asignar a los reportes.
        """
        if asunto in self.baseDeDato:
            for report in self.baseDeDato[asunto]:
                report.prioridad = prioridad


def generar_registros(repositorio, cantidad_registro, asunto):
    """
    Genera y agrega un número especificado de reportes de prueba al repositorio dado.

    Args:
        repositorio (RepositorioDeReporte): El repositorio donde se agregarán los reportes.
        cantidad_registro (int): Número de reportes a generar.
        asunto (str): Asunto de los reportes a generar.
    """
    fake = Faker()

    for _ in range(int(cantidad_registro)):
        ciudadano = Ciudadano(nombre_completo=fake.name(), correo_electronico=fake.email(),
                              numero_identificacion=fake.numerify("###-###-###"))
        tipo_reporte = TipoReporte(asunto=asunto, descripcion=fake.text())
        reporte = Reporte(ciudadano=ciudadano, tipo_reporte=tipo_reporte, ubicacion=fake.address())
        reporte.prioridad = fake.random_int(min=1, max=5)

        repositorio.agregar_reporte(reporte)
