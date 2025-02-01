from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from ..models import Ciudadano
from ..forms import CiudadanoLoginForm

def login_ciudadano(request):
    if request.method == 'POST':
        form = CiudadanoLoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo_electronico']
            password = form.cleaned_data['password']
            
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