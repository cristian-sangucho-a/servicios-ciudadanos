from django.shortcuts import render
from entidad_municipal_app.models import EspacioPublico
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


def agenda(request):
    """
    Vista que muestra la agenda de espacios públicos disponibles.

    Args:
        request (HttpRequest): La solicitud HTTP recibida por Django.

    Steps:
        - Crea una instancia del servicio de reserva.
        - Obtiene todos los espacios públicos disponibles utilizando el servicio de reserva.
        - Renderiza la plantilla `agenda.html` con los espacios públicos como contexto.

    Returns:
        HttpResponse: La respuesta HTTP que renderiza la plantilla `agenda.html` con los datos de los espacios públicos.
    """
    servicio_reserva = ServicioReserva()
    espacios_publicos = servicio_reserva.obtener_espacios_publicos()
    return render(request, 'agenda.html', {
        'espacios_publicos': espacios_publicos
    })