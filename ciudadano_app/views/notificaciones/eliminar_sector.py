from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from ...decorators import ciudadano_required
from shared.models import Sector

@ciudadano_required
def eliminar_sector_ciudadano(request, sector_id):
    ciudadano = request.user
    sector = get_object_or_404(Sector, id=sector_id)

    if request.method == 'POST':
        if sector in ciudadano.sectores_de_interes.all():
            ciudadano.sectores_de_interes.remove(sector)
            messages.success(request, f'Sector {sector.nombre} eliminado de tus intereses.')
        else:
            messages.error(request, 'No puedes eliminar un sector que no está en tu lista de intereses.')
        return redirect('listar_sectores')

    return redirect('listar_sectores')  # En caso de que se acceda por GET, redirigir