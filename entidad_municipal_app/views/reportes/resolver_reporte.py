from django.shortcuts import render, redirect
from django.contrib import messages

from entidad_municipal_app.decorators import entidad_required
from entidad_municipal_app.models.reporte.repositorio_de_reporte_municipal_django import \
    RepositorioDeReporteMunicipalDjango
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal


@entidad_required
def resolver_reporte(request, reporte_id):
    """Vista para redirigir al formulario de evidencia y resolver un reporte municipal.

    Args:
        request (HttpRequest): La solicitud HTTP enviada por el usuario.
        reporte_id (int): El identificador único del reporte municipal a resolver.

    Returns:
        HttpResponse: Si la solicitud es GET, renderiza el formulario para resolver el reporte.
        HttpResponseRedirect: Si la solicitud es POST, redirige a la lista de reportes con un mensaje.

    Raises:
        Exception: Captura cualquier error al intentar cambiar el estado del reporte y muestra un mensaje de error.
    """
    if request.method == "POST":
        # Inicializamos el repositorio y el servicio
        repositorio = RepositorioDeReporteMunicipalDjango()
        servicio_reporte = ServicioReporteMunicipal(repositorio)

        # Obtenemos el reporte por su ID
        reporte = servicio_reporte.obtener_reporte_municipal_por_id(reporte_id)

        # Cambiamos el estado del reporte a "atendiendo"
        try:
            servicio_reporte.atender_reporte_municipal(reporte_id)
            messages.success(request, f'El reporte #{reporte_id} se está atendiendo.')
        except Exception as e:
            print(f"Error {e}")
            messages.error(request, f'No se pudo atender el reporte #{reporte_id}.')

        return redirect('lista_todos_reportes')

    return render(request, 'entidad/reportes/resolver_reporte.html')
