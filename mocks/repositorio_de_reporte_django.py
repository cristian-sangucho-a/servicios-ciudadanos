from faker.proxy import Faker

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

def generar_registros(repositorio ,cantidad_registro, asunto):
    fake = Faker()

    for _ in range(int(cantidad_registro)):
        ciudadano = Ciudadano(nombre_completo=fake.name(), correo_electronico=fake.email(), numero_identificacion=fake.numerify("###-###-###"))
        ciudadano.save()
        tipo_reporte = TipoReporte(asunto=asunto, descripcion=fake.text())
        tipo_reporte.save()

        reporte = Reporte(ciudadano=ciudadano, tipo_reporte=tipo_reporte, ubicacion=fake.address())
        reporte.prioridad = fake.random_int(min=1, max=5)

        repositorio.agregar_reporte(reporte)