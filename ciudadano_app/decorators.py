from functools import wraps
from django.shortcuts import redirect
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from shared.decorators import no_session_required

def ciudadano_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not isinstance(request.user, Ciudadano):
            return redirect('login_ciudadano')
        return view_func(request, *args, **kwargs)
    return wrapper