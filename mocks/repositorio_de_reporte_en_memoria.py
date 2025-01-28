from faker.proxy import Faker

from ciudadano_app.models import Ciudadano
from ciudadano_app.models.reporte.reporte import Reporte
from ciudadano_app.models.reporte.repositorio_de_reporte import RepositorioDeReporte
from ciudadano_app.models.reporte.tipo_reporte import TipoReporte


class RepositorioDeReporteEnMemoria(RepositorioDeReporte):
    def __init__(self):
        self.baseDeDato = {}

    def obtener_reportes_por_asunto(self, asunto: str):
        return self.baseDeDato.get(asunto, [])

    def agregar_reporte(self, reporte: Reporte):
        if reporte.tipo_reporte.asunto not in self.baseDeDato:
            self.baseDeDato[reporte.tipo_reporte.asunto] = []
        self.baseDeDato[reporte.tipo_reporte.asunto].append(reporte)

    def actualizar_prioridad_de_reporte_por_asunto(self, asunto: str, prioridad: int):
        if asunto in self.baseDeDato:
            for report in self.baseDeDato[asunto]:
                report.prioridad = prioridad



def generar_registros(repositorio ,cantidad_registro, asunto):
    fake = Faker()

    for _ in range(int(cantidad_registro)):
        ciudadano = Ciudadano(nombre_completo=fake.name(), correo_electronico=fake.email(), numero_identificacion=fake.numerify("###-###-###"))
        tipo_reporte = TipoReporte(asunto=asunto, descripcion=fake.text())
        reporte = Reporte(ciudadano=ciudadano, tipo_reporte=tipo_reporte, ubicacion=fake.address())
        reporte.prioridad = fake.random_int(min=1, max=5)

        repositorio.agregar_reporte(reporte)
