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
        area_comunal = request.GET.get('area_comunal')
        form = ReservaRegisterForm(initial={
            'fecha_reserva': fecha_reserva,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'ciudadano': ciudadano.id,
            'area_comunal': area_comunal
        })

    return render(request, 'reseva.html', {'form': form})