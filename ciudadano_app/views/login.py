from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..models import Ciudadano

def login_ciudadano(request):
    """Vista para el login de ciudadanos"""
    if request.method == 'POST':
        correo = request.POST.get('correo_electronico')
        password = request.POST.get('password')
            
            user = authenticate(request, correo_electronico=correo, password=password)

            if user is None:
                form.add_error(None, "Credenciales inválidas")
            elif not isinstance(user, Ciudadano):
                form.add_error(None, "Este usuario no es un ciudadano.")
            else:
                login(request, user)
                return redirect('bienvenida_ciudadano')
    else:
        form = CiudadanoLoginForm()
    return render(request, 'login_ciudadano.html', {'form': form})