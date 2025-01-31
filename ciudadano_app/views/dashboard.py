from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Ciudadano  # Asegúrate de importar el modelo Evento
from entidad_municipal_app.models import EventoMunicipal

@login_required
def dashboard_ciudadano(request):
    """Vista de bienvenida después del login"""

    # Obtener el ciudadano relacionado con el usuario actual
    ciudadano = Ciudadano.objects.get(id=request.user.id)

    return render(request, 'dashboard.html', {
        'ciudadano': ciudadano,
    })
