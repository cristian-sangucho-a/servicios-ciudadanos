from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from ...decorators import ciudadano_required
from shared.models import Sector

@ciudadano_required
def agregar_sectores_ciudadano(request):
    if request.method == 'POST':
        sector_id = request.POST.get('sector_id')
        ciudadano = request.user
        try:
            sector = Sector.objects.get(id=sector_id)
            ciudadano.sectores_de_interes.add(sector)
            messages.success(request, f'Sector {sector.nombre} agregado a tus intereses.')
        except ObjectDoesNotExist:
            messages.error(request, 'El sector no existe.')
        return redirect('listar_sectores')
    else:
        sectores = Sector.objects.all()
        return render(request, 'notificaciones/agregar_sectores.html', {'sectores': sectores})
