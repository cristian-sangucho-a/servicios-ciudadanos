from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ..models import EntidadMunicipal

@login_required
def dashboard_entidad(request):
    """Dashboard principal de la entidad municipal"""
    if not isinstance(request.user, EntidadMunicipal):
        messages.error(request, 'Acceso no autorizado')
        return redirect('landing_page')
    
    context = {
        'entidad': request.user
    }
    return render(request, 'entidad/dashboard.html', context)
