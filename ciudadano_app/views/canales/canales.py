from django.shortcuts import render, get_object_or_404

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import Noticia
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo, Suscripcion


def lista_canales(request):
    """
        Lista los canales informativos que no son de emergencia.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.

        Returns:
            HttpResponse: Renderiza la plantilla 'canales/lista_canales.html' con los canales disponibles.
    """
    canales = CanalInformativo.objects.filter(es_emergencia=False)
    return render(request, 'canales/lista_canales.html', {'canales': canales})


def detalle_canal(request, canal_id):
    """
        Muestra los detalles de un canal informativo específico, incluidas sus noticias y la suscripción del usuario.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            canal_id (int): El identificador del canal informativo.

        Returns:
            HttpResponse: Renderiza la plantilla 'canales/detalle_canal.html' con las noticias del canal,
                          el estado de suscripción del usuario y los detalles del canal.

        Raises:
            Ciudadano.DoesNotExist: Si no se encuentra un ciudadano con el ID del usuario autenticado.
            CanalInformativo.DoesNotExist: Si no se encuentra un canal con el ID proporcionado.
    """
    ciudadano = request.user
    canal = get_object_or_404(CanalInformativo,id=canal_id)
    esta_suscrito = canal.esta_suscrito(ciudadano)
    return render(request, 'canales/detalle_canal.html',
                  { 'esta_suscrito': esta_suscrito, 'canal': canal})


def ver_noticias(request):
    """
        Muestra las noticias de los canales a los que el ciudadano está suscrito.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.

        Returns:
            HttpResponse: Renderiza la plantilla 'canales/muro.html' con las noticias de los canales suscritos.

        Raises:
            Ciudadano.DoesNotExist: Si no se encuentra un ciudadano con el ID del usuario autenticado.
    """
    ciudadano = request.user
    noticias = Noticia.obtener_noticias(ciudadano)
    return render(request, 'canales/muro.html', {'noticias': noticias})
