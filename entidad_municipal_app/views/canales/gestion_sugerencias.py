from django.db.models.query_utils import Q
from django.shortcuts import render, redirect, get_object_or_404
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.canales.sugerencia import Sugerencia
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo


def listar_sugerencias(request):
    """
        Muestra una lista de las sugerencias de los ciudadanos.

        Esta vista obtiene las sugerencias de los ciudadanos y las pasa al template para su renderizado.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.

        Returns:
            HttpResponse: El renderizado del template 'canales/lista_sugerencias.html', con la lista de sugerencias.
    """
    sugerencias = Sugerencia.objects.exclude(Q(estado='Rechazada') | Q(estado='Aceptada'))
    #sugerencias = Sugerencia.objects.all()
    return render(request, 'canales/lista_sugerencias.html', {'sugerencias': sugerencias})


def aceptar_sugerencia(request, sugerencia_id):
    """
        Acepta una sugerencia y crea un canal informativo basado en los datos de la sugerencia.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            sugerencia_id (int): El ID de la sugerencia a aceptar.

        Returns:
            HttpResponseRedirect: Redirige a la lista de canales de la entidad municipal después de crear el canal.
    """
    # Obtener la sugerencia por su ID
    sugerencia = get_object_or_404(Sugerencia, id=sugerencia_id)

    # Si la sugerencia ya ha sido aceptada, no se hace nada (o se puede agregar una validación)
    if sugerencia.canal_creado:
        # Si ya se creó un canal, redirige de vuelta a la lista de sugerencias
        return redirect('lista_sugerencias')

    # Crear un canal informativo basado en la sugerencia
    entidad_municipal = request.user  # Suposición de que el usuario es una entidad municipal
    canal_informativo = CanalInformativo.objects.create(
        entidad_municipal=entidad_municipal,
        nombre=sugerencia.nombre,
        descripcion=sugerencia.descripcion,
        es_emergencia=False  # Puedes ajustar este valor según el caso
    )

    # Actualizar la sugerencia para reflejar que el canal fue creado
    sugerencia.canal_creado = True
    sugerencia.estado = 'Aceptada'
    sugerencia.save()

    # Redirigir a la lista de canales después de aceptar la sugerencia
    return redirect('listar_canales_administrados')

def rechazar_sugerencia(request, sugerencia_id):
    """
        Rechaza una sugerencia y marca la sugerencia como rechazada.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.
            sugerencia_id (int): El ID de la sugerencia a rechazar.

        Returns:
            HttpResponseRedirect: Redirige a la lista de sugerencias.
    """
    sugerencia = get_object_or_404(Sugerencia, id=sugerencia_id)
    sugerencia.estado = 'Rechazada'  # Si deseas eliminar la sugerencia completamente
    sugerencia.save()
    return redirect('lista_sugerencias')


