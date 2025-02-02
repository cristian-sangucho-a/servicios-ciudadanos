from xml.etree.ElementTree import tostring
from django.db.models import Count
from django.shortcuts import render, redirect
from entidad_municipal_app.models import Noticia, CanalInformativo, Reaccion, Comentario


def noticias_canal(request,canal_id):
    canal = CanalInformativo.objects.get(id=canal_id)
    noticias = Noticia.objects.filter(canal=canal)
    return render(request,'canales/listado_noticias.html',{'noticias':noticias,'canal':canal})

def crear_noticia(request,canal_id):
    if request.method == 'POST':
        canal = CanalInformativo.objects.get(id=canal_id)
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')

        if titulo and contenido and canal:
            Noticia.objects.create(
                titulo=titulo,
                contenido=contenido,
                imagen=imagen,
                canal=canal
            )
            canal_id_text = str(canal_id)
            return redirect('/entidad_municipal/lista_canales/noticias_canal/'+canal_id_text)
    return noticias_canal(request, canal_id)

def detalle_noticia(request,noticia_id):
    noticia = Noticia.objects.get(id=noticia_id)
    conteos_reacciones = noticia.reacciones.values('tipo').annotate(conteo=Count('tipo'))

    # Crear un diccionario con los conteos de reacciones
    reacciones_dict = {tipo: 0 for tipo, _ in Reaccion.TIPOS_REACCION}
    for conteo in conteos_reacciones:
        reacciones_dict[conteo['tipo']] = conteo['conteo']

    comentarios = Comentario.objects.filter(noticia=noticia)
    return render(request,'canales/detalle_noticia.html', {'noticia':noticia,'reacciones':reacciones_dict,'comentarios':comentarios})

def eliminar_noticia(request, noticia_id):
    noticia = Noticia.objects.get(id=noticia_id)
    canal = noticia.canal
    noticia.delete()
    return redirect('/entidad_municipal/lista_canales/noticias_canal/'+str(canal.id))