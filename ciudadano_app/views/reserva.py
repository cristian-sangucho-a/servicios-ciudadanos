from django.contrib import messages
from django.shortcuts import render, redirect
from ciudadano_app.decorators import ciudadano_required
from ciudadano_app.forms import ReservaRegisterForm
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


@ciudadano_required
def reservar(request):
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
            id_reserva, exito = servicio_reserva.reservar_area_comunal(area_comunal, fecha_reserva, hora_inicio, hora_fin, form.cleaned_data['tipo_reserva'], ciudadano, form.cleaned_data['correos_invitados'])
            if exito:
                messages.success(request, '¡Reserva creada exitosamente!')
                return redirect('mis_reservas')
            else:
                messages.error(request, 'No se pudo crear la reserva')
                return redirect('agenda')
        else:
            messages.error(request, 'No se lleno correctamente el formulario.')

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
    ciudadano = request.user

    if request.method == 'POST':
        id_reserva =  request.POST.get('id_reserva')
        servicio_reserva = ServicioReserva()
        servicio_reserva.cancelar_reserva(id_reserva, ciudadano)

    return redirect('mis_reservas')

@ciudadano_required
def mis_reservas(request):
    ciudadano = request.user
    servicio_reserva = ServicioReserva()
    reservas = servicio_reserva.obtener_reservas_activas_ciudadano(ciudadano)
    return render(request, 'mis_reservas.html', {'reservas': reservas})

