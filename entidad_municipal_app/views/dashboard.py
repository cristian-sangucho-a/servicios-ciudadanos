from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ..models import EntidadMunicipal
from ..decorators import entidad_required

@entidad_required
def dashboard_entidad(request):
    """Dashboard principal de la entidad municipal"""
    context = {
        'entidad': request.user
    }
    return render(request, 'entidad/dashboard.html', context)
