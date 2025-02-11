from xml.etree.ElementTree import tostring
from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from entidad_municipal_app.models import Noticia, CanalInformativo, Reaccion, Comentario


def noticias_canal(request,canal_id):
    """
        Muestra las noticias de un canal informativo específico.

        Esta vista obtiene todas las noticias asociadas a un canal informativo y las pasa al template para su visualización.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            canal_id (int): El identificador del canal informativo cuyas noticias se desean mostrar.

        Returns:
            HttpResponse: El renderizado del template 'canales/listado_noticias.html', con la lista de noticias.
    """
    canal = get_object_or_404(CanalInformativo,id=canal_id)
    return render(request,'canales/listado_noticias.html',{'canal':canal})

def crear_noticia(request,canal_id):
    """
        Crea una nueva noticia para un canal informativo específico.

        Esta vista maneja el formulario para la creación de una noticia. Al recibir una solicitud POST, crea una nueva noticia
        asociada al canal especificado y redirige a la lista de noticias del canal.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario que contiene los datos del formulario.
            canal_id (int): El identificador del canal al cual se asociará la nueva noticia.

        Returns:
            HttpResponseRedirect: Redirige a la lista de noticias del canal después de crear la noticia.
    """
    if request.method == 'POST':
        canal = get_object_or_404(CanalInformativo,id=canal_id)
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')

        if titulo and contenido and canal:
            Noticia.crear_noticia(canal,titulo,contenido,imagen)
    return noticias_canal(request, canal_id)

def detalle_noticia(request,noticia_id):
    """
        Muestra el detalle de una noticia específica, incluyendo el conteo de reacciones y los comentarios.

        Esta vista obtiene la noticia especificada por su ID, los conteos de las reacciones para esa noticia, y los comentarios
        asociados. Luego, los pasa al template para su renderizado.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            noticia_id (int): El identificador de la noticia cuyo detalle se desea mostrar.

        Returns:
            HttpResponse: El renderizado del template 'canales/detalle_noticia.html', con los detalles de la noticia.
    """
    noticia = get_object_or_404(Noticia,id=noticia_id)
    reacciones_dict = noticia.contar_reacciones()
    return render(request,'canales/detalle_noticia.html', {'noticia':noticia,'reacciones':reacciones_dict})

def eliminar_noticia(request, noticia_id):
    """
        Elimina una noticia específica.

        Esta vista recibe el identificador de una noticia, la elimina de la base de datos y redirige a la lista de noticias
        del canal al que pertenecía la noticia eliminada.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            noticia_id (int): El identificador único de la noticia a eliminar.

        Returns:
            HttpResponseRedirect: Redirige a la lista de noticias del canal después de eliminar la noticia.
    """
    noticia = get_object_or_404(Noticia,id=noticia_id)
    canal = noticia.canal
    noticia.delete()
    return redirect('/entidad_municipal/lista_canales/noticias_canal/'+str(canal.id))

def alerta_de_emergencia(request,canal_id):
    """
        Envía una alerta de emergencia a los ciudadanos suscritos al canal informativo.

        Esta vista maneja el envío de alertas de emergencia. Al recibir una solicitud POST, crea una alerta de emergencia
        asociada al canal especificado, y notifica a todos los ciudadanos suscritos a dicho canal.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario que contiene los datos de la alerta.
            canal_id (int): El identificador del canal al cual se enviará la alerta de emergencia.

        Returns:
            HttpResponseRedirect: Redirige a la lista de canales después de enviar la alerta de emergencia.
    """
    if request.method == 'POST':
        canal = get_object_or_404(CanalInformativo,id=canal_id)
        incidente = request.POST.get('incidente')
        localidad = request.POST.get('localidad')

        if incidente and localidad and canal:
            canal.notificar_alerta_emergencia(incidente, localidad)
    return redirect('/entidad_municipal/lista_canales/')