from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def bienvenida_ciudadano(request):
    """Vista de bienvenida después del login"""
    return render(request, 'bienvenida.html')