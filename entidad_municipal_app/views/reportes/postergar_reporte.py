from django.shortcuts import redirect
from django.contrib import messages
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal

def postergar_reporte(request, reporte_id):
    if request.method == "POST":
        # Inicializar el repositorio y el servicio de reporte municipal
        repositorio = RepositorioDeReporteMunicipalEnMemoria()
        servicio_reporte = ServicioReporteMunicipal(repositorio)

        # Obtener el reporte a través del servicio
        reporte = servicio_reporte.obtener_reporte_municipal_por_id(reporte_id)
        print("este es el estado que llega " , reporte.obtener_estado())

        # Verificar si el estado del reporte es 'postergado'
        if reporte.estado == "postergado":
            # Si ya está postergado, mostrar un mensaje de error
            messages.error(request, "Este reporte ya ha sido postergado.")
        else:
            # Intentar postergar el reporte
            if servicio_reporte.postergar_reporte(reporte_id):
                messages.success(request, "El reporte ha sido postergado exitosamente.")
            else:
                messages.error(request, "No se pudo postergar el reporte.")

    # Redirigir a la vista de ver reportes
    return redirect('lista_todos_reportes')