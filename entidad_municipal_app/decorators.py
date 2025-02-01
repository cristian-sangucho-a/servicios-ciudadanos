from functools import wraps
from django.shortcuts import redirect, render
from entidad_municipal_app.models import EntidadMunicipal
from ciudadano_app.models import Ciudadano

def entidad_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica que el usuario esté autenticado y que sea una instancia de EntidadMunicipal
        if not request.user.is_authenticated or not isinstance(request.user, EntidadMunicipal):
            return redirect('login_entidad')
        return view_func(request, *args, **kwargs)
    return wrapper

def no_session_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Si el usuario está autenticado, redirige a la página de error
        if request.user.is_authenticated:
            if isinstance(request.user, EntidadMunicipal):
                return_url = '/entidad/dashboard/'
            elif isinstance(request.user, Ciudadano):
                return_url = '/ciudadano/dashboard/'
            else:
                return_url = '/'
            
            return render(request, 'error_session.html', {
                'return_url': return_url
            })
        return view_func(request, *args, **kwargs)
    return wrapper
