from django.shortcuts import render
from django.utils.dateparse import postgres_interval_re

from entidad_municipal_app.models.reporte.reporte_municipal import ReporteMunicipal
from mocks.repositorio_de_departamento_en_memoria import RepositorioDeDepartamentoEnMemoria
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria


def lista_todos_reportes(request):
    """Vista para listar todos los reportes municipales."""
    repositorio_reportes = RepositorioDeReporteMunicipalEnMemoria()
    repositorio_departamentos = RepositorioDeDepartamentoEnMemoria()

    # Obtener todos los reportes y departamentos
    todos_reportes = repositorio_reportes.obtener_todos()
    departamentos = repositorio_departamentos.listar_departamentos()

    if todos_reportes:  # Verifica si hay reportes en la lista
        primer_reporte = todos_reportes[4]  # Obtiene el primer elemento
        print("estado inicial" , primer_reporte.obtener_estado())
        primer_reporte.estado = "postergado"  # Cambia el estado del reporte a "asignado"
        print("estado inicial" , primer_reporte.obtener_estado())

    else:
        print("No hay reportes disponibles")


    return render(request, 'entidad/reportes/lista_reportes.html', {
        'reportes': todos_reportes,
        'departamentos': departamentos
    })