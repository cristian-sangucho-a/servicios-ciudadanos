from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required


@entidad_required
def cancelar_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, id=evento_id)

    # Cargar el estado más reciente
    if evento.espacio_publico:
        evento.espacio_publico.refresh_from_db()

    if request.method == 'POST':
        motivo_cancelacion = request.POST.get('motivo_cancelacion')

        print("Estado actual del incidente:", evento.espacio_publico.estado_incidente_espacio)  # Debugging

        if evento.espacio_publico and evento.espacio_publico.estado_incidente_espacio == 'AFECTADO':
            if motivo_cancelacion:
                evento.estado_actual = EventoMunicipal.ESTADO_CANCELADO
                evento.motivo_cancelacion = motivo_cancelacion
                evento.save()
                messages.success(request, 'El evento ha sido cancelado exitosamente.')
                return redirect('gestor_eventos')
            else:
                messages.error(request, 'Debe proporcionar un motivo de cancelación.')
        else:
            messages.error(request, 'El evento no puede ser cancelado porque el espacio público no está afectado.')

    return render(request, 'entidad/eventos/cancelar_evento.html', {'evento': evento})
