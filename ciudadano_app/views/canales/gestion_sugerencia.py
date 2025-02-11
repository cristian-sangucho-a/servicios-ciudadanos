from contextlib import nullcontext
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.canales.sugerencia import Sugerencia

from django.contrib import messages
from django.shortcuts import redirect



def crear_sugerencia(request):
    """
    Crea un nuevo canal informativo y lo suscribe a todos los ciudadanos si es de emergencia.
    """
    if request.method == 'POST':
        ciudadano = request.user
        entidad_municipal = EntidadMunicipal.objects.get(id=1)
        nombre = request.POST.get('nombre_sugerencia')
        descripcion = request.POST.get('descripcion')

        # Verificar si ya existe un canal con el mismo nombre
        if Sugerencia.objects.filter(nombre=nombre).exists():
            # Pasar el mensaje de error en el contexto
            return render(request, 'canales/crear_sugerencia.html', {
                'nombre_sugerencia': nombre,
                'descripcion': descripcion,
                'modal_error': 'Ya existe un canal con este nombre. Por favor, elige otro nombre.',
            })
        elif nombre and descripcion:
            Sugerencia.crear_sugerencia_canal(nombre, descripcion, ciudadano, entidad_municipal)
            messages.success(request, 'La sugerencia de canal ha sido creada exitosamente.')
            return redirect('/ciudadano/lista_canales')

    # Si no es POST, mostrar el formulario vacío
    return render(request, 'canales/crear_sugerencia.html')

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