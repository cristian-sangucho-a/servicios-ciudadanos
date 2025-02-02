from django.shortcuts import render

from entidad_municipal_app.decorators import entidad_required
from entidad_municipal_app.models.departamento.servicio_departamento import ServicioDepartamento
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal
from mocks.repositorio_de_departamento_en_memoria import RepositorioDeDepartamentoEnMemoria
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria

@entidad_required
def lista_reportes_por_departamento(request,departamento=None):
    """Vista para listar reportes municipales filtrados por departamento."""
    repositorio_reportes = RepositorioDeReporteMunicipalEnMemoria()
    repositorio_departamentos = RepositorioDeDepartamentoEnMemoria()
    servicio_de_reporte = ServicioReporteMunicipal(repositorio_reportes)
    servicio_de_departamento = ServicioDepartamento(repositorio_departamentos)

    # Obtener todos los reportes y departamentos
    todos_reportes = servicio_de_reporte.obtener_reportes_municipales()
    departamentos = servicio_de_departamento.obtener_departamentos()

    # Filtrar por departamento si viene en los parámetros
    if departamento:
        reportes_filtrados = [reporte for reporte in todos_reportes if reporte.obtener_departamento() and reporte.obtener_departamento().nombre.upper() == departamento.upper()]

    else:
        reportes_filtrados = todos_reportes

    return render(request, 'entidad/reportes/lista_reportes_por_departamento.html', {
        'reportes': reportes_filtrados,
        'departamentos': departamentos,
        'departamento_seleccionado': departamento
    })