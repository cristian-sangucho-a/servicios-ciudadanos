from django.shortcuts import render
from mocks.repositorio_de_departamento_en_memoria import RepositorioDeDepartamentoEnMemoria
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria

def lista_reportes_por_departamento(request,departamento=None):
    """Vista para listar reportes municipales filtrados por departamento."""
    repositorio_reportes = RepositorioDeReporteMunicipalEnMemoria()
    repositorio_departamentos = RepositorioDeDepartamentoEnMemoria()

    # Obtener todos los reportes y departamentos
    todos_reportes = repositorio_reportes.obtener_todos()
    departamentos = repositorio_departamentos.listar_departamentos()

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