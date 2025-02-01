from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib import messages

def logout_usuario(request):
    """Vista compartida para cerrar sesión de cualquier tipo de usuario"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('landing_page')
