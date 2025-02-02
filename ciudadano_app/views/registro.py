from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from ..forms import CiudadanoRegisterForm
from ..models import Ciudadano


def registro_ciudadano(request):
    """Vista para el registro de nuevos ciudadanos"""
    if request.method == 'POST':
        form = CiudadanoRegisterForm(request.POST)
        if form.is_valid():
            nombre_completo = request.POST.get('nombre_completo')
            correo_electronico = request.POST.get('correo_electronico')
            numero_identificacion = request.POST.get('numero_identificacion')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')

            if password != password2:
                messages.error(request, 'Las contraseñas no coinciden')
                return redirect('registro_ciudadano')

            if Ciudadano.objects.filter(correo_electronico=correo_electronico).exists():
                messages.error(request, 'Este correo electrónico ya está registrado')
                return redirect('registro_ciudadano')

            Ciudadano.objects.create_user(
                correo_electronico=correo_electronico,
                password=password,
                nombre_completo=nombre_completo,
                numero_identificacion=numero_identificacion,
            )

            messages.success(request, 'Registro exitoso. Por favor inicia sesión.')
            return redirect('landing_page')
        else:
            messages.error(request, 'Registro invalido. Por favor verifica los datos ingresados.')

    return render(request, 'registro_ciudadano.html')
