from django.shortcuts import redirect
from django.http import JsonResponse
from django.shortcuts import render
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import Reaccion, Noticia, Comentario
from django.db.models import Count
from django.http import HttpResponse


def reaccionar(request, noticia_id):
    if request.method == 'POST':
        noticia = Noticia.objects.get(id=noticia_id)
        ciudadano = Ciudadano.objects.get(id=request.user.id)
        tipo_reaccion = request.POST.get('tipo_reaccion')
        if tipo_reaccion:
            Reaccion.objects.create(
                noticia=noticia,
                ciudadano=ciudadano,
                tipo=tipo_reaccion
            )
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_ciudadano'))

def comentar(request, noticia_id):
    if request.method == 'POST':
        noticia = Noticia.objects.get(id=noticia_id)
        ciudadano = Ciudadano.objects.get(id=request.user.id)
        comentario_texto = request.POST.get('comentario_texto')
        Comentario.objects.update_or_create(
            noticia=noticia,
            ciudadano=ciudadano,
            contenido=comentario_texto
        )
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_ciudadano'))


def conteo_reacciones(request, noticia_id):
    noticia = Noticia.objects.get(id=noticia_id)
    conteos_reacciones = noticia.reacciones.values('tipo').annotate(conteo=Count('tipo'))

    # Crear un diccionario con los conteos de reacciones
    reacciones_dict = {tipo: 0 for tipo, _ in Reaccion.TIPOS_REACCION}
    for conteo in conteos_reacciones:
        reacciones_dict[conteo['tipo']] = conteo['conteo']
    return JsonResponse({'reacciones': reacciones_dict})
