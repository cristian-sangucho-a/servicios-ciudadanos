from django.shortcuts import render


def cargar_calendario(request):
    """
    Vista que carga el calendario de un área comunal específica.

    Args:
        request (HttpRequest): La solicitud HTTP recibida por Django.
                               Se espera que contenga un parámetro GET llamado `area_id`.

    Steps:
        - Obtiene el ID del área comunal desde los parámetros GET de la solicitud.
        - Renderiza la plantilla `calendario_area.html` con el ID del área como contexto.

    Returns:
        HttpResponse: La respuesta HTTP que renderiza la plantilla `calendario_area.html`
                      con el ID del área comunal como contexto.
    """
    area_id = request.GET.get('area_id')
    return render(request, 'calendario_area.html', {
        'area_id': area_id
    })

