from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from entidad_municipal_app.models import EventoMunicipal
from entidad_municipal_app.models.evento.evento_municipal import ErrorGestionEventos
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia


def lista_eventos(request):
    eventos = EventoMunicipal.objects.filter(fecha_realizacion__gte=timezone.now())
    
    if request.user.is_authenticated:
        for evento in eventos:
            # Verificar si el usuario está inscrito
            try:
                registro = RegistroAsistencia.objects.get(evento=evento, ciudadano=request.user)
                evento.is_subscribed = registro.estado_registro == RegistroAsistencia.ESTADO_INSCRITO
            except RegistroAsistencia.DoesNotExist:
                evento.is_subscribed = False
    
    return render(request, 'eventos/lista_eventos.html', {'eventos': eventos})

@login_required
def inscribirse_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, pk=evento_id)
    try:
        registro = evento.inscribir_ciudadano(request.user)
        if registro.estado_registro == RegistroAsistencia.ESTADO_INSCRITO:
            messages.success(request, 'Te has inscrito exitosamente al evento.')
        else:
            messages.info(request, 'Has sido agregado a la lista de espera del evento.')
    except ErrorGestionEventos as e:
        messages.error(request, str(e))
    return redirect('lista_eventos')

@login_required
def cancelar_inscripcion(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, pk=evento_id)
    try:
        registro = RegistroAsistencia.objects.get(evento=evento, ciudadano=request.user)
        evento.cancelar_inscripcion(registro.id)
        messages.success(request, 'Tu inscripción ha sido cancelada exitosamente.')
    except (RegistroAsistencia.DoesNotExist, ErrorGestionEventos) as e:
        messages.error(request, str(e))
    return redirect('lista_eventos')

@login_required
def lista_espera_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, pk=evento_id)
    try:
        registro = evento.inscribir_ciudadano(request.user)
        messages.info(request, 'Has sido agregado a la lista de espera del evento.')
    except ErrorGestionEventos as e:
        messages.error(request, str(e))
    return redirect('lista_eventos')
