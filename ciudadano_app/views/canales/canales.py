from django.shortcuts import render

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import Noticia
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo, Suscripcion


def lista_canales(request):
    canales = CanalInformativo.objects.filter(es_emergencia=False)
    return render(request, 'canales/lista_canales.html', {'canales': canales})


def detalle_canal(request, canal_id):
    ciudadano = Ciudadano.objects.get(id=request.user.id)
    canal = CanalInformativo.objects.get(id=canal_id)
    noticias = Noticia.objects.filter(canal=canal)
    esta_suscrito = Suscripcion.objects.filter(canal=canal, ciudadano=ciudadano).exists()
    return render(request, 'canales/detalle_canal.html',
                  {'noticias': noticias, 'esta_suscrito': esta_suscrito, 'canal': canal})


def ver_noticias(request):
    ciudadano = Ciudadano.objects.get(id=request.user.id)
    canales = (CanalInformativo.objects.filter(suscripciones__ciudadano=ciudadano))
    noticias = (Noticia.objects.filter(canal__in=canales))
    return render(request, 'canales/muro.html', {'noticias': noticias})
