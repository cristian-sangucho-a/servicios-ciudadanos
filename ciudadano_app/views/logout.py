from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout

def logout_ciudadano(request):
    """Vista para cerrar sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('landing_page')
