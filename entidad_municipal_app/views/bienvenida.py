from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def bienvenida_entidad(request):
    """Vista de bienvenida para la entidad municipal"""
    return render(request, 'entidad/bienvenida.html')
