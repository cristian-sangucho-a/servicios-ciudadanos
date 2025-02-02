from django.shortcuts import render
from ciudadano_app.models import AreaComunal
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva

def cargar_areas(request):
    servicio_reserva = ServicioReserva()
    espacio_id = request.GET.get('espacio_id')
    areas_comunales = servicio_reserva.obtener_areas_comunales_por_espacio(espacio_id)
    return render(request, 'areas_comunales.html', {
        'areas_comunales': areas_comunales
    })