from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria


def agregar_evidencia(request, reporte_id):
    repositorio = RepositorioDeReporteMunicipalEnMemoria()
    servicio_reporte = ServicioReporteMunicipal(repositorio)

    reporte = repositorio.obtener_por_id(reporte_id)

    if not reporte:
        messages.error(request, "Reporte no encontrado.")
        return redirect('lista_todos_reportes')

    # Manejar la solicitud POST
    if request.method == 'POST':
        comentario = request.POST.get('comentario', '').strip()
        if not comentario:
            messages.error(request, "El comentario es obligatorio para resolver el reporte.")
        else:
            # Registrar la evidencia y cambiar el estado a 'resuelto'
            servicio_reporte.registrar_evidencia(reporte, comentario)
            messages.success(request, "El reporte ha sido resuelto exitosamente.")
            return redirect('lista_todos_reportes')

    return render(request, 'entidad/reportes/resolver_reporte.html', {'reporte': reporte})
