from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Ciudadano

def login_ciudadano(request):
    """Vista para el login de ciudadanos"""
    if request.method == 'POST':
        correo = request.POST.get('correo_electronico')
        password = request.POST.get('password')
        
        # Prints de depuración
        print("="*50)
        print("DATOS DE LOGIN RECIBIDOS:")
        print(f"Correo electrónico: {correo}")
        print(f"Contraseña ingresada: {password}")
        
        # Verificar si el usuario existe
        try:
            ciudadano = Ciudadano.objects.get(correo_electronico=correo)
            print("\nUSUARIO ENCONTRADO EN LA BASE DE DATOS:")
            print(f"Nombre: {ciudadano.nombre_completo}")
            print(f"Correo: {ciudadano.correo_electronico}")
            print(f"¿Está activo?: {ciudadano.esta_activo}")
        except Ciudadano.DoesNotExist:
            print("\nUSUARIO NO ENCONTRADO EN LA BASE DE DATOS")
            
        user = authenticate(request, correo_electronico=correo, password=password)
        print("\nRESULTADO DE AUTENTICACIÓN:")
        print(f"Usuario autenticado: {'Sí' if user is not None else 'No'}")
        print("="*50)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Has iniciado sesión exitosamente.')
            return redirect('landing_page')
        else:
            messages.error(request, 'Credenciales inválidas. Por favor intenta de nuevo.')
    
    return render(request, 'ciudadano/login_ciudadano.html')

def registro_ciudadano(request):
    """Vista para el registro de nuevos ciudadanos"""
    if request.method == 'POST':
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
        
    return render(request, 'ciudadano/registro_ciudadano.html')

@login_required
def bienvenida_ciudadano(request):
    """Vista de bienvenida después del login"""
    return render(request, 'bienvenida.html')

def logout_ciudadano(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('landing_page')
