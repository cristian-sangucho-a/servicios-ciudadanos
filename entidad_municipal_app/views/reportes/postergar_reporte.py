from django.shortcuts import redirect
from django.contrib import messages

from entidad_municipal_app.decorators import entidad_required
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal

@entidad_required
def postergar_reporte(request, reporte_id):
    if request.method == "POST":
        # Inicializar el repositorio y el servicio de reporte municipal
        repositorio = RepositorioDeReporteMunicipalEnMemoria()
        servicio_reporte = ServicioReporteMunicipal(repositorio)

        # Obtener el reporte a través del servicio
        reporte = servicio_reporte.obtener_reporte_municipal_por_id(reporte_id)

        try:
            servicio_reporte.postergar_reporte(reporte_id)
        except Exception as e:
            print(f"Error {e}")
            estado = reporte.obtener_estado()
            messages.error(request, f"No se pudo postergar el reporte ya que está {estado}")

    # Redirigir a la vista de ver reportes
    return redirect('lista_todos_reportes')