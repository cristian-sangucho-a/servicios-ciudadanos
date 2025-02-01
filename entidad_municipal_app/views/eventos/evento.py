from django.shortcuts import render
from django.utils import timezone
from entidad_municipal_app.models import EventoMunicipal
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def evento(request):
    """Vista para listar todos los eventos activos."""
    context = {
        'entidad': request.user
    }
    return render(request, 'entidad/eventos/evento.html', context)