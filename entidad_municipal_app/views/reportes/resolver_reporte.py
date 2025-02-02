from django.shortcuts import render, redirect
from django.contrib import messages

from entidad_municipal_app.decorators import entidad_required
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal


@entidad_required
def resolver_reporte(request, reporte_id):
    """Vista para redirigir al formulario de evidencia y resolver reporte."""
    if request.method == "POST":
        # Inicializamos el repositorio y el servicio
        repositorio = RepositorioDeReporteMunicipalEnMemoria()
        servicio_reporte = ServicioReporteMunicipal(repositorio)

        # Obtenemos el reporte por su ID
        reporte = servicio_reporte.obtener_reporte_municipal_por_id(reporte_id)


        # Cambiamos el estado del reporte a "atendiendo"
        try:
            servicio_reporte.atender_reporte_municipal(reporte_id)
            messages.success(request, f'El reporte #{reporte_id} se está atendiendo.')
        except:
            messages.error(request , f'No se pudo atender el reporte #{reporte_id}.')

        return redirect('lista_todos_reportes')

    return render(request, 'entidad/reportes/resolver_reporte.html')