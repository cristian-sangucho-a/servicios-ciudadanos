from django.shortcuts import render
from django.utils.dateparse import postgres_interval_re

from entidad_municipal_app.decorators import entidad_required
from entidad_municipal_app.models.reporte.reporte_municipal import ReporteMunicipal
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal
from mocks.repositorio_de_departamento_en_memoria import RepositorioDeDepartamentoEnMemoria
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria
from entidad_municipal_app.models.departamento.servicio_departamento import ServicioDepartamento

@entidad_required
def lista_todos_reportes(request):
    """Vista para listar todos los reportes municipales."""
    repositorio_reportes = RepositorioDeReporteMunicipalEnMemoria()
    repositorio_departamentos = RepositorioDeDepartamentoEnMemoria()
    servicio_de_reporte = ServicioReporteMunicipal(repositorio_reportes)
    servicio_de_departamento = ServicioDepartamento(repositorio_departamentos)

    # Obtener todos los reportes y departamentos
    todos_reportes = servicio_de_reporte.obtener_reportes_municipales()
    departamentos = servicio_de_departamento.obtener_departamentos()

    return render(request, 'entidad/reportes/lista_reportes.html', {
        'reportes': todos_reportes,
        'departamentos': departamentos
    })