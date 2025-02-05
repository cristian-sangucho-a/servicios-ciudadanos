from collections import OrderedDict
from django.shortcuts import render
from shared.models.reporte.reporte import Reporte
from shared.models import ServicioDeReporte, RepositorioDeReporteDjango

repositorioReporte = RepositorioDeReporteDjango()
servicioDeReporte = ServicioDeReporte(repositorioReporte)

def reportes_view(request):
    # Retrieve all reports and order them by asunto (for grouping) and then by prioridad in descending order
    sorted_grouped_reportes = servicioDeReporte.obetener_lista_reportes_por_asunto()
    
    return render(request, 'reporte/reportes.html', {'reportes_grouped': sorted_grouped_reportes})
