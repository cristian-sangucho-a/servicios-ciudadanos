from functools import wraps
from django.shortcuts import redirect
from entidad_municipal_app.models import EntidadMunicipal
from shared.decorators import no_session_required

def entidad_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verifica que el usuario esté autenticado y que sea una instancia de EntidadMunicipal
        if not request.user.is_authenticated or not isinstance(request.user, EntidadMunicipal):
            return redirect('login_entidad')
        return view_func(request, *args, **kwargs)
    return wrapper
