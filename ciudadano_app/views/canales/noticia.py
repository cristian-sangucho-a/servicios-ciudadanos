from django.shortcuts import redirect, get_object_or_404
from django.http import JsonResponse
from django.shortcuts import render
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import Reaccion, Noticia, Comentario
from django.db.models import Count
from django.http import HttpResponse


def reaccionar(request, noticia_id):
    """
        Registra una reacción de un ciudadano a una noticia específica.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            noticia_id (int): El identificador de la noticia a la que se reacciona.

        Returns:
            HttpResponseRedirect: Redirige a la página anterior o al dashboard del ciudadano.

        Raises:
            Noticia.DoesNotExist: Si la noticia con el ID proporcionado no existe.
            Ciudadano.DoesNotExist: Si el ciudadano con el ID del usuario autenticado no existe.
    """
    if request.method == 'POST':
        noticia = get_object_or_404(Noticia,id=noticia_id)
        ciudadano = request.user
        tipo_reaccion = request.POST.get('tipo_reaccion')
        if tipo_reaccion:
            noticia.reaccionar(ciudadano,tipo_reaccion)
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_ciudadano'))

def comentar(request, noticia_id):
    """
        Permite a un ciudadano comentar en una noticia específica.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            noticia_id (int): El identificador de la noticia en la que se realizará el comentario.

        Returns:
            HttpResponseRedirect: Redirige a la página anterior o al dashboard del ciudadano.

        Raises:
            Noticia.DoesNotExist: Si la noticia con el ID proporcionado no existe.
            Ciudadano.DoesNotExist: Si el ciudadano con el ID del usuario autenticado no existe.
    """
    if request.method == 'POST':
        noticia = get_object_or_404(Noticia,id=noticia_id)
        ciudadano = request.user
        comentario_texto = request.POST.get('comentario_texto')
        if comentario_texto:
            noticia.comentar(ciudadano,comentario_texto)
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_ciudadano'))


def conteo_reacciones(request, noticia_id):
    """
        Obtiene el conteo de reacciones de una noticia específica.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            noticia_id (int): El identificador de la noticia cuyos conteos de reacciones se desean obtener.

        Returns:
            JsonResponse: Un diccionario JSON con el conteo de cada tipo de reacción.

        Raises:
            Noticia.DoesNotExist: Si la noticia con el ID proporcionado no existe.
    """
    noticia = get_object_or_404(Noticia,id = noticia_id)
    reacciones_dict=noticia.contar_reacciones()
    return JsonResponse({'reacciones': reacciones_dict})

