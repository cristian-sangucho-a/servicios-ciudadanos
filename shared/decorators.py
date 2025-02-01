from functools import wraps
from django.shortcuts import redirect, render
from entidad_municipal_app.models import EntidadMunicipal
from ciudadano_app.models import Ciudadano

def no_session_required(view_func):
    """
    Decorator compartido que verifica que no haya una sesión activa
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
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
