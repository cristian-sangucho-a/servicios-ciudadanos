from django.http import JsonResponse
from datetime import datetime
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


def obtener_reservas_por_fecha(request):
    """
    Vista que obtiene las reservas de un área comunal para una fecha específica.

    Args:
        request (HttpRequest): La solicitud HTTP recibida por Django. 
                               Se espera que contenga los parámetros GET `fecha` y `area_comunal_id`.

    Steps:
        - Obtiene la fecha y el ID del área comunal desde los parámetros GET de la solicitud.
        - Convierte la fecha de string a un objeto `date`.
        - Utiliza el servicio de reserva para obtener el área comunal correspondiente al ID proporcionado.
        - Si no se encuentra el área comunal, retorna una respuesta JSON con un mensaje de error y estado 404.
        - Obtiene las reservas activas para el área comunal y la fecha especificada.
        - Formatea los datos de las reservas en una lista de diccionarios.
        - Retorna una respuesta JSON con los datos de las reservas.

    Returns:
        JsonResponse: Una respuesta JSON que contiene:
            - Las reservas en formato de lista de diccionarios si se encuentran.
            - Un mensaje de error si el área comunal no existe.

    Raises:
        ValueError: Si ocurre un error al convertir la fecha (no debería ocurrir si el formato es correcto).
    """
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