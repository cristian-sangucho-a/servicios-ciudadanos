from django.shortcuts import render
from ..decorators import ciudadano_required

@ciudadano_required
def dashboard_ciudadano(request):
    """Vista de bienvenida después del login"""

    # Obtener el ciudadano relacionado con el usuario actual
    ciudadano = Ciudadano.objects.get(id=request.user.id)

    return render(request, 'dashboard.html', {
        'ciudadano': ciudadano,
    })
