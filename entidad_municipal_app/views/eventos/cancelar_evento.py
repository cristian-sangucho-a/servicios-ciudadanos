from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import ValidationError
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.espacio_publico import EspacioPublico
from entidad_municipal_app.models.evento.enums import EstadoEvento
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def cancelar_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, id=evento_id)

    # Verificar que el evento no esté ya cancelado
    if evento.estado_actual == EstadoEvento.CANCELADO.value:
        messages.error(request, "Este evento ya está cancelado.")
        return redirect('gestor_eventos')

    # Verificar que el evento tenga un espacio público asignado
    if not evento.espacio_publico:
        messages.error(request, "Este evento no tiene un espacio público asignado.")
        return redirect('gestor_eventos')

    if request.method == 'POST':
        motivo_cancelacion = request.POST.get('motivo_cancelacion', '').strip()
        estado_incidente = request.POST.get('estado_incidente_espacio')

        # Validar que se haya seleccionado un estado para el incidente
        if not estado_incidente:
            messages.error(request, "Debe seleccionar un estado para el incidente del espacio público.")
            return render(request, 'entidad/eventos/cancelar_evento.html', {'evento': evento})

        # Validar que el motivo de cancelación no esté vacío
        if not motivo_cancelacion:
            messages.error(request, "Debe proporcionar un motivo de cancelación.")
            return render(request, 'entidad/eventos/cancelar_evento.html', {'evento': evento})

        try:
            # Si el espacio está afectado, proceder con la cancelación
            if estado_incidente == EspacioPublico.AFECTADO:
                # Actualizar el estado del evento
                evento.set_motivo_cancelacion(motivo_cancelacion)
                
                # Actualizar el estado del espacio público
                espacio = evento.espacio_publico
                espacio.marcar_como_afectado()
                espacio.marcar_como_disponible()  # Liberar el espacio para futuros eventos
                
                messages.success(request, 'El evento ha sido cancelado exitosamente.')
                return redirect('gestor_eventos')
            else:
                messages.error(request, 'El evento solo puede ser cancelado si el espacio público está afectado.')
                return render(request, 'entidad/eventos/cancelar_evento.html', {'evento': evento})

        except ValidationError as e:
            messages.error(request, f'Error de validación: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error al cancelar el evento: {str(e)}')

    return render(request, 'entidad/eventos/cancelar_evento.html', {'evento': evento})