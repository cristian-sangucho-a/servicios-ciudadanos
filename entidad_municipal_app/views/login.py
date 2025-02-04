from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from ..forms import EntidadLoginForm
from ..models import EntidadMunicipal
from ..decorators import no_session_required

@no_session_required
def login_entidad(request):
    if request.method == 'POST':
        form = EntidadLoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo_electronico']
            password = form.cleaned_data['password']
            
            # Verificar si existe el usuario en la base de datos
            try:
                entidad = EntidadMunicipal.objects.get(correo_electronico=correo)
            except EntidadMunicipal.DoesNotExist:
                entidad = None
            
            # Autenticar usando username (que es el correo_electronico)
            user = authenticate(request, username=correo, password=password)
            
            if user is None:
                if entidad:
                    form.add_error(None, "Credenciales inválidas")
            elif not isinstance(user, EntidadMunicipal):
                form.add_error(None, "Este usuario no es una entidad municipal.")
            else:
                login(request, user)
                return redirect('dashboard_entidad')
    else:
        form = EntidadLoginForm()
    return render(request, 'entidad/login_entidad.html', {'form': form})