from django.shortcuts import render, redirect
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def cancelar_evento(request, evento_id):
    evento = EventoMunicipal.objects.get(id=evento_id)

    # Obtener el estado_incidente_espacio desde el modelo relacionado (ajusta esto según tu modelo)
    estado_incidente_espacio = evento.espacio_publico.estado_incidente_espacio if evento.espacio_publico else None

    if request.method == 'POST':
        # Obtener el nuevo estado del incidente desde el formulario
        nuevo_estado = request.POST.get('estado_incidente_espacio')

        if nuevo_estado:
            # Actualizar el estado en el modelo
            if evento.espacio_publico:
                evento.espacio_publico.estado_incidente_espacio = nuevo_estado
                evento.espacio_publico.save()

            # Volver a cargar el evento con el estado actualizado
            estado_incidente_espacio = nuevo_estado
            return redirect('cancelar_evento', evento_id=evento.id)

    # Pasar la información al contexto de la plantilla
    return render(request, 'entidad/eventos/cancelar_evento.html', {
        'evento': evento,
        'estado_incidente_espacio': estado_incidente_espacio
    })
