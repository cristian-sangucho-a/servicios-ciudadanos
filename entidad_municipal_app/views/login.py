from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from ..forms import EntidadLoginForm
from ..models import EntidadMunicipal

def login_entidad(request):
    if request.method == 'POST':
        form = EntidadLoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo_electronico']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=correo, password=password)
            
            if user is None:
                form.add_error(None, "Credenciales inválidas")
            elif not isinstance(user, EntidadMunicipal):
                form.add_error(None, "Este usuario no es una entidad municipal.")
            else:
                login(request, user)
                return redirect('dashboard_entidad')
    else:
        form = EntidadLoginForm()
    return render(request, 'entidad/login_entidad.html', {'form': form})