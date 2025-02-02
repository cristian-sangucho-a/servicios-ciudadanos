from django.shortcuts import render, redirect
from django.contrib import messages
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal


def resolver_reporte(request, reporte_id):
    """Vista para redirigir al formulario de evidencia y resolver reporte."""
    if request.method == "POST":
        # Inicializamos el repositorio y el servicio
        repositorio = RepositorioDeReporteMunicipalEnMemoria()
        servicio_reporte = ServicioReporteMunicipal(repositorio)

        # Obtenemos el reporte por su ID
        reporte = repositorio.obtener_por_id(reporte_id)

        # Cambiamos el estado del reporte a "atendiendo"
        reporte.cambiar_estado("atendiendo")
        messages.success(request, f'El reporte #{reporte_id} ha pasado a "atendiendo".')
        # Redirigimos a la lista de todos los reportes
        return redirect('lista_todos_reportes')
