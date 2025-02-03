from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def actualizar_estado_incidente_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, id=evento_id)

    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_incidente_espacio')

        if nuevo_estado and evento.espacio_publico:
            evento.espacio_publico.estado_incidente_espacio = nuevo_estado
            evento.espacio_publico.save()

            # Recargar el objeto después de guardarlo
            evento.refresh_from_db()

            # Mensaje de éxito para retroalimentación
            messages.success(request, f"Estado actualizado a {nuevo_estado}")

            # Redirigir para reflejar los cambios
            return redirect('cancelar_evento', evento_id=evento.id)

    # Obtener el estado actualizado
    estado_incidente_espacio = evento.espacio_publico.estado_incidente_espacio if evento.espacio_publico else None

    return render(request, 'entidad/eventos/cancelar_evento.html', {
        'evento': evento,
        'estado_incidente_espacio': estado_incidente_espacio
    })

