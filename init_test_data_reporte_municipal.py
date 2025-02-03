import django
import os

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servicios_ciudadanos.settings")
django.setup()

from faker import Faker
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models.departamento.departamento import Departamento
from entidad_municipal_app.models.reporte.reporte_municipal import ReporteMunicipal
from shared.models.reporte.tipo_reporte import TipoReporte
from shared.models.reporte.reporte import Reporte
from entidad_municipal_app.models.reporte.repositorio_de_reporte_municipal_django import RepositorioDeReporteMunicipalDjango

fake = Faker("es_ES")


def reset_db():
    """Elimina todos los datos previos en la base de datos"""
    print("Reseteando base de datos...")
    Ciudadano.objects.all().delete()
    Departamento.objects.all().delete()
    TipoReporte.objects.all().delete()
    Reporte.objects.all().delete()
    ReporteMunicipal.objects.all().delete()


def crear_ciudadanos(n=10):
    """Crea ciudadanos de prueba"""
    print("Creando ciudadanos...")
    ciudadanos = []
    for _ in range(n):
        ciudadano = Ciudadano.objects.create(
            nombre_completo=fake.name(),
            correo_electronico=fake.email(),
            numero_identificacion=fake.numerify(text="##########"),
            password="password123",
        )
        ciudadanos.append(ciudadano)
    return ciudadanos


def crear_departamentos():
    """Crea departamentos en la base de datos"""
    print("Creando departamentos...")
    nombres_departamentos = [
        "EPMMOP",
        "Obras Públicas",
        "Seguridad Ciudadana",
        "Medio Ambiente",
        "Desarrollo Urbano",
        "Servicios Públicos",
        "Gestión de Riesgos",
    ]

    departamentos = []
    for nombre in nombres_departamentos:
        departamento = Departamento.objects.create(
            nombre=nombre,
            descripcion=fake.sentence(nb_words=10),
        )
        departamentos.append(departamento)
    return departamentos


def crear_tipos_reporte(departamentos):
    """Crea tipos de reporte y los asigna a departamentos"""
    print("Creando tipos de reporte...")
    tipos_reporte = []
    for _ in range(10):
        tipo = TipoReporte.objects.create(
            asunto=fake.sentence(nb_words=4),
            descripcion=fake.text(max_nb_chars=200),
            departamento=fake.random_element(departamentos),
            prioridad_de_atencion=fake.random_int(min=1, max=3),
        )
        tipos_reporte.append(tipo)
    return tipos_reporte


def crear_reportes(ciudadanos, tipos_reporte):
    """Crea reportes ciudadanos"""
    print("Creando reportes ciudadanos...")
    reportes = []
    for _ in range(15):
        reporte = Reporte.objects.create(
            ciudadano=fake.random_element(ciudadanos),
            tipo_reporte=fake.random_element(tipos_reporte),
            ubicacion=fake.address(),
            prioridad=fake.random_int(min=1, max=5),
        )
        reportes.append(reporte)
    return reportes


def crear_reportes_municipales(reportes):
    """Crea reportes municipales a partir de los reportes ciudadanos"""
    print("Creando reportes municipales...")
    repo_reportes = RepositorioDeReporteMunicipalDjango()
    estados_validos = ["no_asignado", "asignado", "atendiendo", "resuelto", "postergado"]

    for reporte in reportes:
        estado = fake.random_element(estados_validos)
        repo_reportes.crear(reporte_ciudadano=reporte)
        print(f"Reporte municipal creado con estado: {estado}")


if __name__ == "__main__":
    reset_db()
    ciudadanos = crear_ciudadanos()
    departamentos = crear_departamentos()
    tipos_reporte = crear_tipos_reporte(departamentos)
    reportes = crear_reportes(ciudadanos, tipos_reporte)
    crear_reportes_municipales(reportes)
    print("Base de datos inicializada con datos de prueba correctamente.")
