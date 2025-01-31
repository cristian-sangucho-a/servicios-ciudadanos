from django.shortcuts import render
from django.utils import timezone
from entidad_municipal_app.models import EventoMunicipal

def lista_eventos(request):
    """Vista para listar todos los eventos activos."""
    eventos = EventoMunicipal.objects.filter(
        fecha_realizacion__gte=timezone.now(),
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    ).order_by('fecha_realizacion')
    
    return render(request, 'entidad/eventos/lista_eventos.html', {
        'eventos': eventos
    })