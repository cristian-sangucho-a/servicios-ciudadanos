from django.shortcuts import render
from ..decorators import ciudadano_required
from entidad_municipal_app.models import EventoMunicipal
from entidad_municipal_app.models import RegistroAsistencia


@ciudadano_required
def dashboard_ciudadano(request):
    ciudadano = request.user
    eventos_inscritos = EventoMunicipal.objects.filter(
        registroasistencia__ciudadano=ciudadano,
        registroasistencia__estado_registro__in=[
            RegistroAsistencia.ESTADO_INSCRITO,
            RegistroAsistencia.ESTADO_EN_ESPERA
        ]
    ).distinct()

    return render(request, 'dashboard.html', {
        'ciudadano': ciudadano,
        'eventos_inscritos': eventos_inscritos
    })
