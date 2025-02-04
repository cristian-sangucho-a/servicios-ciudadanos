from django.shortcuts import render
from ciudadano_app.models import AreaComunal
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


def cargar_areas(request):
    """
    Vista que carga las áreas comunales asociadas a un espacio público específico.

    Args:
        request (HttpRequest): La solicitud HTTP recibida por Django.
                               Se espera que contenga un parámetro GET llamado `espacio_id`.

    Steps:
        - Crea una instancia del servicio de reserva.
        - Obtiene el ID del espacio público desde los parámetros GET de la solicitud.
        - Utiliza el servicio de reserva para obtener las áreas comunales asociadas al espacio público.
        - Renderiza la plantilla `areas_comunales.html` con las áreas comunales como contexto.

    Returns:
        HttpResponse: La respuesta HTTP que renderiza la plantilla `areas_comunales.html`
                      con los datos de las áreas comunales asociadas al espacio público.
    """
    servicio_reserva = ServicioReserva()
    espacio_id = request.GET.get('espacio_id')
    areas_comunales = servicio_reserva.obtener_areas_comunales_por_espacio(espacio_id)
    return render(request, 'areas_comunales.html', {
        'areas_comunales': areas_comunales
    })