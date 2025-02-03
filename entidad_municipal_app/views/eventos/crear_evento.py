from django.shortcuts import render, redirect
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required

@entidad_required
@login_required
def crear_evento(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_evento = request.POST.get('nombre_evento')
        descripcion_evento = request.POST.get('descripcion_evento')
        fecha_realizacion = request.POST.get('fecha_realizacion')
        lugar_evento = request.POST.get('lugar_evento')
        capacidad_maxima = request.POST.get('capacidad_maxima')

        # Crear una nueva instancia de EventoMunicipal
        nuevo_evento = EventoMunicipal(
            nombre_evento=nombre_evento,
            descripcion_evento=descripcion_evento,
            fecha_realizacion=fecha_realizacion,
            lugar_evento=lugar_evento,
            capacidad_maxima=capacidad_maxima
        )
        nuevo_evento.save()  # Guardar el evento en la base de datos

        # Redirigir a la página de gestión de eventos o a donde desees
        return redirect('gestor_eventos')  # Asegúrate de que 'gestor_eventos' sea el nombre correcto de tu URL

    return render(request, 'entidad/eventos/crear_evento.html')