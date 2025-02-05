from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from ...decorators import ciudadano_required
from shared.models.sector import Sector


@ciudadano_required
def eliminar_sector_ciudadano(request, sector_id):
    ciudadano = request.user
    sector = get_object_or_404(Sector, id=sector_id)

    if request.method == 'POST':
        # Verificar si el sector está en los intereses del ciudadano
        if sector not in ciudadano.sectores_de_interes.all():
            messages.error(request, 'No puedes eliminar un sector que no está en tu lista de intereses.')
            return redirect('listar_sectores')

        # Verificar que no sea el último sector
        if ciudadano.sectores_de_interes.count() <= 1:
            messages.error(request, 'Debes mantener al menos un sector de interés.')
            return redirect('listar_sectores')

        # Si pasa las validaciones, eliminar el sector
        ciudadano.sectores_de_interes.remove(sector)
        messages.success(request, f'Sector {sector.nombre} eliminado de tus intereses.')
        return redirect('listar_sectores')

    return redirect('listar_sectores')  # En caso de que se acceda por GET, redirigir