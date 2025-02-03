from django.shortcuts import render, redirect, get_object_or_404
from entidad_municipal_app.models import EspacioPublico
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required
from django.contrib import messages  # Para mostrar mensajes

@entidad_required
@login_required
def espacios_publicos_disponibles(request):
    espacios = None  # Inicializa espacios como None

    if request.method == 'POST':
        fecha = request.POST.get('fecha_realizacion')
        espacio_publico = EspacioPublico.objects.get(pk=request.POST.get('espacio_publico'))
        espacios = EspacioPublico.obtener_espacios_disponibles(fecha)

        # Imprimir los espacios obtenidos para depuración
        print(f"Espacios disponibles para la fecha {fecha}: {espacios}")

        if not espacios.exists():
            messages.warning(request, 'No hay espacios disponibles para la fecha seleccionada.')

    return render(request, 'entidad/eventos/espacios_disponibles.html', {
        'espacios': espacios
    })