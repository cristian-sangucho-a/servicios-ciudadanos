from django.shortcuts import render, redirect
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required
from django.contrib import messages


@entidad_required
def editar_evento(request, evento_id):
    evento = EventoMunicipal.objects.get(id=evento_id)
    try:
        if request.method == 'POST':
            evento.nombre_evento = request.POST.get('nombre_evento')
            evento. descripcion_evento = request.POST.get('descripcion_evento')
            evento.fecha_realizacion = request.POST.get('fecha_realizacion')
            evento.capacidad_maxima = request.POST.get('capacidad_maxima')
            evento.save()
            messages.success(request, 'El evento se ha editado exitosamente.')
            return redirect('gestor_eventos')
    except Exception as e:
        messages.error(request, f'Error al crear el evento: {str(e)}')

    return render(request, 'entidad/eventos/editar_evento.html',{'evento': evento})