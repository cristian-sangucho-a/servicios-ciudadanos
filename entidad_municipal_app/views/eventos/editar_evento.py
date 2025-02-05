from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.decorators import entidad_required

@entidad_required
@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, id=evento_id)
    try:
        if request.method == 'POST':
            evento.nombre_evento = request.POST.get('nombre_evento')
            evento.descripcion_evento = request.POST.get('descripcion_evento')  # Sin espacio extra
            evento.fecha_realizacion = request.POST.get('fecha_realizacion')
            # Convertir la capacidad a entero
            capacidad_maxima = request.POST.get('capacidad_maxima')
            try:
                evento.capacidad_maxima = int(capacidad_maxima)
            except ValueError:
                messages.error(request, 'La capacidad máxima debe ser un número válido.')
                return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})
            
            evento.save()
            messages.success(request, 'El evento se ha editado exitosamente.')
            return redirect('gestor_eventos')
    except Exception as e:
        messages.error(request, f'Error al editar el evento: {str(e)}')

    return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})