from django.contrib import messages
from django.shortcuts import render, redirect
from ciudadano_app.decorators import ciudadano_required
from ciudadano_app.forms import ReservaRegisterForm
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


@ciudadano_required
def reservar(request):
    """
    Vista que permite a un ciudadano realizar una reserva en un área comunal.

    Args:
        request (HttpRequest): La solicitud HTTP recibida por Django.
                               Se espera que contenga los parámetros GET `fecha_reserva`, `hora_inicio`,
                               `hora_fin` y `area_comunal`.

    Steps:
        - Obtiene los datos necesarios para la reserva desde los parámetros GET.
        - Si la solicitud es POST, valida el formulario y realiza la reserva utilizando el servicio de reserva.
        - Si la reserva es exitosa, redirige al usuario a la página de "mis reservas".
        - Si la solicitud no es POST, inicializa el formulario con los datos proporcionados.
        - Renderiza la plantilla `reserva.html` con el formulario y el área comunal como contexto.

    Returns:
        HttpResponse: La respuesta HTTP que renderiza la plantilla `reserva.html` o redirige al usuario.
    """
    ciudadano: Ciudadano = request.user
    servicio_reserva = ServicioReserva()
    fecha_reserva = request.GET.get('fecha_reserva', '')
    hora_inicio = request.GET.get('hora_inicio', '')
    hora_fin = request.GET.get('hora_fin', '')
    area_comunal_id = request.GET.get('area_comunal', '')
    area_comunal = servicio_reserva.obtener_area_comunal(area_comunal_id)
    if request.method == 'POST':
        form = ReservaRegisterForm(request.POST)
        if form.is_valid():
            _, exito = servicio_reserva.reservar_area_comunal(
                area_comunal, fecha_reserva, hora_inicio, hora_fin,
                form.cleaned_data['tipo_reserva'], ciudadano,
                form.cleaned_data['correos_invitados']
            )
            if exito:
                messages.success(request, '¡Reserva creada exitosamente!')
                return redirect('mis_reservas')
            else:
                messages.error(request, 'No se pudo crear la reserva. Superaste el maximo de reservas activas.')
                return redirect('agenda')
        else:
            messages.error(request, 'No se llenó correctamente el formulario.')
    else:
        initial_data = {
            'fecha_reserva': fecha_reserva,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'area_comunal': area_comunal.id,
            'ciudadano': ciudadano.id,
            'estado_reserva': "Activa"
        }
        form = ReservaRegisterForm(initial=initial_data)
    return render(request, 'reserva.html', {
        'form': form,
        'area_comunal': area_comunal
    })


@ciudadano_required
def cancelar_reserva(request):
    """
    Vista que permite a un ciudadano cancelar una reserva existente.

    Args:
        request (HttpRequest): La solicitud HTTP recibida por Django.
                               Se espera que sea una solicitud POST con el parámetro `id_reserva`.

    Steps:
        - Obtiene el ID de la reserva desde los parámetros POST.
        - Utiliza el servicio de reserva para cancelar la reserva.
        - Redirige al usuario a la página de "mis reservas".

    Returns:
        HttpResponse: La respuesta HTTP que redirige al usuario a la página de "mis reservas".
    """
    ciudadano = request.user
    if request.method == 'POST':
        id_reserva = request.POST.get('id_reserva')
        servicio_reserva = ServicioReserva()
        servicio_reserva.cancelar_reserva(id_reserva, ciudadano)
    return redirect('mis_reservas')


@ciudadano_required
def mis_reservas(request):
    """
    Vista que muestra las reservas activas de un ciudadano.

    Args:
        request (HttpRequest): La solicitud HTTP recibida por Django.

    Steps:
        - Obtiene el ciudadano autenticado.
        - Utiliza el servicio de reserva para obtener las reservas activas del ciudadano.
        - Renderiza la plantilla `mis_reservas.html` con las reservas como contexto.

    Returns:
        HttpResponse: La respuesta HTTP que renderiza la plantilla `mis_reservas.html`
                      con las reservas activas del ciudadano.
    """
    ciudadano = request.user
    servicio_reserva = ServicioReserva()
    reservas = servicio_reserva.obtener_reservas_activas_ciudadano(ciudadano)
    return render(request, 'mis_reservas.html', {'reservas': reservas})

