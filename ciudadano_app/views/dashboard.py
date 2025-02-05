from django.shortcuts import render
from django.utils import timezone
from ..decorators import ciudadano_required
from entidad_municipal_app.models import EventoMunicipal, RegistroAsistencia
from entidad_municipal_app.models.evento.enums import EstadoRegistro, EstadoEvento

@ciudadano_required
def dashboard_ciudadano(request):
    ciudadano = request.user
    ahora = timezone.now()

    # Eventos donde estoy inscrito
    eventos_inscritos = EventoMunicipal.objects.filter(
        registroasistencia_set__ciudadano=ciudadano,
        registroasistencia_set__estado_registro=EstadoRegistro.INSCRITO.value
    ).distinct().count()

    # Eventos donde estoy en lista de espera
    eventos_en_espera = EventoMunicipal.objects.filter(
        registroasistencia_set__ciudadano=ciudadano,
        registroasistencia_set__estado_registro=EstadoRegistro.EN_ESPERA.value
    ).distinct().count()

    # Total de eventos activos en el sistema
    total_eventos = EventoMunicipal.objects.filter(
        fecha_realizacion__gte=ahora,
        estado_actual__in=[EstadoEvento.PROGRAMADO.value, EstadoEvento.EN_CURSO.value]
    ).count()

    context = {
        'ciudadano': ciudadano,
        # Eventos metrics
        'eventos_inscritos': eventos_inscritos,
        'eventos_en_espera': eventos_en_espera,
        'total_eventos': total_eventos,
        
        # Placeholder metrics for other sections
        'reportes_enviados': 0,
        'reportes_en_proceso': 0,
        'canales_suscritos': 0,
        'mensajes_sin_leer': 0,
        'total_reservaciones': 0,
        'reservaciones_proximas': 0,
        
        # For alerts section (placeholder for now)
        'alertas': [],
    }
    
    return render(request, 'dashboard.html', context)
