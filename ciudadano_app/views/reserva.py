from datetime import datetime

from django.shortcuts import render, redirect
from pyexpat.errors import messages

from ciudadano_app.decorators import ciudadano_required
from ciudadano_app.forms import ReservaRegisterForm
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva

@ciudadano_required
def reserva(request):
    ciudadano = request.user

    if request.method == 'POST':
        form = ReservaRegisterForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.ciudadano = ciudadano
            reserva.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('dashboard_ciudadano')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        fecha_reserva = request.GET.get('fecha_reserva')
        hora_inicio = request.GET.get('hora_inicio')
        hora_fin = request.GET.get('hora_fin')
        area_comunal_id = request.GET.get('area_comunal')
        servicio_reserva = ServicioReserva()
        area_comunal = servicio_reserva.obtener_area_comunal(area_comunal_id)
        form = ReservaRegisterForm(initial={
            'fecha_reserva': fecha_reserva,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'ciudadano': ciudadano.id,
            'area_comunal': area_comunal
        })

    return render(request, 'reseva.html', {'form': form})


@ciudadano_required
def cancelar_reserva(request):
    ciudadano = request.user

    if request.method == 'POST':
        id_reserva =  request.POST.get('id_reserva')

        servicio_reserva = ServicioReserva()

        servicio_reserva.cancelar_reserva(id_reserva, ciudadano)

    return render(request, 'agenda.html')


@ciudadano_required
def mis_reservas(request):
    ciudadano = request.user
    servicio_reserva = ServicioReserva()
    reservas = servicio_reserva.obtener_reservas_activas_ciudadano(ciudadano)
    return render(request, 'mis_reservas.html', {'reservas': reservas})

