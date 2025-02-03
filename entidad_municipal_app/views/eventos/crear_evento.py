from django.shortcuts import render, redirect
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required
from django.contrib import messages
from entidad_municipal_app.models.espacio_publico import EspacioPublico

@entidad_required
@login_required
def crear_evento(request):
    espacios = EspacioPublico.objects.all()
    if request.method == 'POST':
        nombre_evento = request.POST.get('nombre_evento')
        descripcion_evento = request.POST.get('descripcion_evento')
        fecha_realizacion = request.POST.get('fecha_realizacion')
        espacio_publico = EspacioPublico.objects.get(pk=request.POST.get('espacio_publico'))
        capacidad_maxima = request.POST.get('capacidad_maxima')
        entidad_municipal = request.user

        try:
            EventoMunicipal.objects.crear_evento_con_aforo(
                nombre=nombre_evento,
                descripcion=descripcion_evento,
                fecha=fecha_realizacion,
                lugar=espacio_publico.direccion,
                capacidad=capacidad_maxima,
                entidad_municipal=entidad_municipal,
                espacio_publico=espacio_publico
            )
            messages.success(request, 'El evento se ha creado exitosamente.')
            return redirect('gestor_eventos')
        except Exception as e:
            messages.error(request, f'Error al crear el evento: {str(e)}')

    return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios})