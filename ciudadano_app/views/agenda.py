from django.shortcuts import render
from entidad_municipal_app.models import EspacioPublico
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva

def agenda(request):
    servicio_reserva = ServicioReserva()
    espacios_publicos = servicio_reserva.obtener_espacios_publicos()
    return render(request, 'agenda.html', {
        'espacios_publicos': espacios_publicos
    })