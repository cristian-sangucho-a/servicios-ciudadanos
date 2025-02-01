from datetime import datetime

from django.shortcuts import render, redirect
from pyexpat.errors import messages

from ciudadano_app.forms import ReservaRegisterForm
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva


def reserva(request):
    if request.method == 'POST':
        form = ReservaRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reserva creada exitosamente.')
            return redirect('dashboard_ciudadano')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        fecha_reserva = request.GET.get('fecha_reserva')
        hora_inicio = request.GET.get('hora_inicio')
        hora_fin = request.GET.get('hora_fin')
        form = ReservaRegisterForm(initial={
            'fecha_reserva': fecha_reserva,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin
        })

    return render(request, 'reseva.html', {'form': form})