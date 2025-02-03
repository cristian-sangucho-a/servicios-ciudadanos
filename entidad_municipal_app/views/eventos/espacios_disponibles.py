from django.shortcuts import render, redirect, get_object_or_404
from entidad_municipal_app.models import EspacioPublico
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required
from django.contrib import messages  # Para mostrar mensajes

@entidad_required
@login_required
def espacios_publicos_disponibles(request):
    espacios = None  # Cambiar el nombre de la variable

    if request.method == 'POST':
        fecha = request.POST.get('fecha')

        espacios = EspacioPublico.obtener_espacios_disponibles(fecha)  # Cambiar aquí también

        espacio_publico_id = request.POST.get('espacio_publico')

        if espacio_publico_id:
            espacio_publico = get_object_or_404(EspacioPublico, pk=espacio_publico_id)

            if espacio_publico.estado_espacio_publico != EspacioPublico.ESTADO_DISPONIBLE:
                messages.error(request, 'El espacio público seleccionado no está disponible en la fecha especificada.')
            else:
                messages.success(request, 'El espacio público está disponible.')


    espacios = EspacioPublico.obtener_espacios_disponibles(None)  # Cambiar aquí también

    return render(request, 'entidad/eventos/.html', {
        'espacios': espacios
    })