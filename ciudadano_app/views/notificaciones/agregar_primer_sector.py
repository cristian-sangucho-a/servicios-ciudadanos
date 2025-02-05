from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from shared.models.sector import Sector

@login_required
def agregar_primer_sector(request):
    if request.user.sectores_de_interes.exists():
        return redirect('dashboard_ciudadano')
        
    if request.method == 'POST':
        sector_id = request.POST.get('sector')
        if sector_id:
            try:
                sector = Sector.objects.get(nombre=sector_id)
                request.user.sectores_de_interes.add(sector)
                messages.success(request, 'Sector de interés agregado exitosamente.')
                return redirect('dashboard_ciudadano')
            except Sector.DoesNotExist:
                messages.error(request, 'El sector seleccionado no es válido.')
        else:
            messages.error(request, 'Debes seleccionar un sector de interés para continuar.')
    
    # Obtener la lista de sectores desde las opciones definidas en el modelo
    sectores = [(sector[0], sector[1]) for sector in Sector.SECTORES]
    
    return render(request, 'notificaciones/agregar_primer_sector.html', {
        'sectores': sectores
    }) 