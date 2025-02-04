# archivo: entidad_municipal_app/views/dashboard.py (o donde tengas la vista definida)
from django.shortcuts import render
from ..decorators import entidad_required
from ..models import EntidadMunicipal
# Importa los modelos que necesites para las métricas
from ..models.evento.evento_municipal import EventoMunicipal
from ..models.canales.canal_informativo import CanalInformativo
from ..models.reporte.repositorio_de_reporte_municipal_django import RepositorioDeReporteMunicipalDjango
from ..models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal

@entidad_required
def dashboard_entidad(request):
    """Dashboard principal de la entidad municipal, con métricas."""
    entidad = request.user  # Entendiendo que request.user es la EntidadMunicipal
    
    # Métrica 1: número total de eventos creados por esta entidad
    total_eventos = EventoMunicipal.objects.filter(entidad_municipal=entidad).count()

    # Métrica 2: número total de canales creados por esta entidad
    total_canales = CanalInformativo.objects.filter(entidad_municipal=entidad).count()

    # Métrica 3: número total de reportes
    repositorio_reportes = RepositorioDeReporteMunicipalDjango()
    servicio_reporte = ServicioReporteMunicipal(repositorio_reportes)
    total_reportes = len(servicio_reporte.obtener_reportes_municipales())
    
    context = {
        'entidad': entidad,
        'total_eventos': total_eventos,
        'total_canales': total_canales,
        'total_reportes': total_reportes
    }
    return render(request, 'entidad/dashboard.html', context)
