from contextlib import nullcontext

from django.shortcuts import render, redirect, get_object_or_404

from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.canales.sugerencia import Sugerencia


def crear_sugerencia(request):
    """
        Crea un nuevo canal informativo y lo suscribe a todos los ciudadanos si es de emergencia.

        Esta vista maneja el formulario de creación de un canal. Al recibir una solicitud POST, crea un nuevo canal
        informativo basado en los datos enviados en el formulario.
        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario que contiene los datos del formulario.

        Returns:
            HttpResponseRedirect: Redirige a la lista de canales de la entidad municipal después de crear el canal.
    """
    if request.method == 'POST':
        ciudadano = request.user
        entidad_municipal = EntidadMunicipal.objects.get(id=1)
        nombre = request.POST.get('nombre_sugerencia')
        descripcion = request.POST.get('descripcion')
        if nombre and descripcion:
            Sugerencia.crear_sugerencia_canal(nombre,descripcion, ciudadano, entidad_municipal)

    print(Sugerencia.objects.all())
    return redirect('/ciudadano/dashboard')

def crear_sugerencia_form(request):
    """
        Muestra el formulario para crear un nuevo canal informativo.

        Esta vista solo renderiza el template que contiene el formulario de creación de un canal.

        Args:
            request (HttpRequest): La solicitud HTTP realizada por el usuario.

        Returns:
            HttpResponse: El renderizado del template 'canales/crear_canal.html', con el formulario para crear un canal.
    """
    return render(request, 'canales/crear_sugerencia.html')