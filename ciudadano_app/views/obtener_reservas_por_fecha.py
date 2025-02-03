# views.py
from django.http import JsonResponse
from datetime import datetime

from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


def obtener_reservas_por_fecha(request):
    fecha = request.GET.get('fecha')
    area_comunal_id = request.GET.get('area_comunal_id')  # Cambiado de area_id a area_comunal_id
    servicio_reserva = ServicioReserva()
    fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    area_comunal = servicio_reserva.obtener_area_comunal(area_comunal_id)
    if not area_comunal:
        return JsonResponse({'error': 'Área comunal no encontrada'}, status=404)
    reservas = servicio_reserva.obtener_reservas_area_comunal(
        area_comunal=area_comunal,
        fecha=fecha_obj
    )
    reservas_data = [{
        'id': reserva.id,
        'hora_inicio': reserva.hora_inicio.strftime('%H:%M'),
        'hora_fin': reserva.hora_fin.strftime('%H:%M'),
        'ciudadano': reserva.ciudadano.nombre_completo,
    } for reserva in reservas]
    return JsonResponse({'reservas': reservas_data})
