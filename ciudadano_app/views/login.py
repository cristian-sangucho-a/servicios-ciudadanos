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
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesión exitosamente.')
            return redirect('dashboard_ciudadano')
        else:
            messages.error(request, 'Credenciales inválidas. Por favor intenta de nuevo.')
    
    return render(request, 'login_ciudadano.html')
