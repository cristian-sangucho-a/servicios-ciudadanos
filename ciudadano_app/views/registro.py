from django.shortcuts import render, redirect
from django.contrib import messages
from ..forms import CiudadanoRegisterForm

def registro_ciudadano(request):
    """Vista para el registro de nuevos ciudadanos utilizando el formulario para la validación."""
    if request.method == 'POST':
        form = CiudadanoRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # El formulario se encarga de la validación y de encriptar la contraseña
            messages.success(request, 'Registro exitoso. Por favor inicia sesión.')
            return redirect('landing_page')
        else:
            messages.error(request, 'Registro inválido. Por favor verifica los datos ingresados.')
    else:
        form = CiudadanoRegisterForm()
        
    return render(request, 'registro_ciudadano.html', {'form': form})