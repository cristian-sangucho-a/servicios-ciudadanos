from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..decorators import ciudadano_required

@ciudadano_required
def bienvenida_ciudadano(request):
    """Vista de bienvenida después del login"""
    return render(request, 'bienvenida.html')