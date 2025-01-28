"""
Vistas para la aplicación de entidad municipal.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from .models.evento_municipal import EventoMunicipal
from .models.registro_asistencia import RegistroAsistencia
from .services import GestorRegistroAsistencia, ErrorGestionEventos

def lista_eventos(request):
    """Vista para listar todos los eventos activos."""
    eventos = EventoMunicipal.objects.filter(
        fecha_realizacion__gte=timezone.now(),
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    ).order_by('fecha_realizacion')
    
    return render(request, 'entidad/eventos/lista_eventos.html', {
        'eventos': eventos
    })

def detalle_evento(request, evento_id):
    """Vista para mostrar los detalles de un evento específico."""
    evento = get_object_or_404(EventoMunicipal, pk=evento_id)
    
    # Si el usuario está autenticado, verificar si ya está inscrito
    if request.user.is_authenticated:
        registro = RegistroAsistencia.objects.filter(
            evento=evento,
            ciudadano=request.user
        ).first()
    else:
        registro = None
    
    return render(request, 'entidad/eventos/detalle_evento.html', {
        'evento': evento,
        'registro': registro
    })

@login_required
def inscribir_evento(request, evento_id):
    """Vista para procesar la inscripción a un evento."""
    if request.method != 'POST':
        return redirect('lista_eventos')
    
    evento = get_object_or_404(EventoMunicipal, pk=evento_id)
    gestor = GestorRegistroAsistencia()
    
    try:
        registro = gestor.procesar_solicitud_inscripcion(
            evento_id=evento.id,
            ciudadano=request.user
        )
        
        if registro.estado_registro == RegistroAsistencia.ESTADO_INSCRITO:
            messages.success(
                request,
                'Te has inscrito exitosamente al evento.'
            )
        else:
            messages.info(
                request,
                'Has sido agregado a la lista de espera del evento.'
            )
            
    except ErrorGestionEventos as e:
        messages.error(request, str(e))
    
    return redirect('detalle_evento', evento_id=evento_id)

@login_required
def cancelar_inscripcion(request, registro_id):
    """Vista para cancelar una inscripción a un evento."""
    if request.method != 'POST':
        return redirect('lista_eventos')
    
    registro = get_object_or_404(
        RegistroAsistencia,
        pk=registro_id,
        ciudadano=request.user
    )
    
    gestor = GestorRegistroAsistencia()
    
    try:
        registro_cancelado, registro_promovido = gestor.procesar_cancelacion_inscripcion(
            registro_id=registro.id
        )
        
        messages.success(request, 'Tu inscripción ha sido cancelada exitosamente.')
        
    except ErrorGestionEventos as e:
        messages.error(request, str(e))
    
    return redirect('detalle_evento', evento_id=registro.evento.id)

@login_required
def lista_espera(request, evento_id):
    """Vista para unirse a la lista de espera de un evento."""
    if request.method != 'POST':
        return redirect('lista_eventos')
    
    evento = get_object_or_404(EventoMunicipal, pk=evento_id)
    gestor = GestorRegistroAsistencia()
    
    try:
        registro = gestor.procesar_solicitud_inscripcion(
            evento_id=evento.id,
            ciudadano=request.user
        )
        
        messages.info(
            request,
            'Has sido agregado a la lista de espera del evento.'
        )
        
    except ErrorGestionEventos as e:
        messages.error(request, str(e))
    
    return redirect('detalle_evento', evento_id=evento_id)
