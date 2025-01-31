"""
Vistas para la aplicación de entidad municipal.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import EntidadLoginForm
from .backends import EntidadBackend
from .models import EntidadMunicipal

def login_entidad(request):
    """Vista para el login de la entidad municipal"""
    if request.method == 'POST':
        form = EntidadLoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo_electronico']
            password = form.cleaned_data['password']
            user = authenticate(request, correo_electronico=correo, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Bienvenido/a')
                return redirect('landing_page')
            else:
                messages.error(request, 'Credenciales inválidas')
    else:
        form = EntidadLoginForm()
    return render(request, 'entidad/login_entidad.html', {'form': form})

@login_required
def bienvenida_entidad(request):
    """Vista de bienvenida para la entidad municipal"""
    return render(request, 'entidad/bienvenida.html')

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
