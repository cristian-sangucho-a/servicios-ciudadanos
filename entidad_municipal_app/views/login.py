from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from ..forms import EntidadLoginForm


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