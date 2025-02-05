from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.enums import EstadoEvento
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def cancelar_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, id=evento_id)

    if not evento.espacio_publico:
        messages.error(request, "Este evento no tiene un espacio público asignado.")
        return redirect('gestor_eventos')

    if request.method == 'POST':
        motivo_cancelacion = request.POST.get('motivo_cancelacion')
        estado_incidente = request.POST.get('estado_incidente_espacio')  # Captura el valor seleccionado

        if not estado_incidente:
            messages.error(request, "Debe seleccionar un estado para el incidente del espacio público.")
            return redirect('gestor_eventos')

        # Si el espacio está afectado y se proporciona un motivo, se cancela el evento
        if estado_incidente == 'AFECTADO':
            if motivo_cancelacion:
                evento.estado_actual = EstadoEvento.CANCELADO.value
                evento.motivo_cancelacion = motivo_cancelacion
                evento.save()
                # Actualizar el estado del espacio público
                evento.espacio_publico.estado_incidente_espacio = estado_incidente
                evento.espacio_publico.save()
                messages.success(request, 'El evento ha sido cancelado exitosamente.')
                return redirect('gestor_eventos')
            else:
                messages.error(request, 'Debe proporcionar un motivo de cancelación.')
        else:
            messages.error(request, 'El evento no puede ser cancelado porque el espacio público no está afectado.')

    return render(request, 'entidad/eventos/cancelar_evento.html', {'evento': evento})