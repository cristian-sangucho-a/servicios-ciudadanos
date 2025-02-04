from collections import OrderedDict
from django.shortcuts import render
from shared.models.reporte.reporte import Reporte

def reportes_view(request):
    # Retrieve all reports and order them by asunto (for grouping) and then by prioridad in descending order
    reportes = Reporte.objects.all().order_by('tipo_reporte__asunto', '-prioridad')
    
    grouped_reportes = {}
    for reporte in reportes:
        asunto = reporte.tipo_reporte.asunto
        if asunto not in grouped_reportes:
            grouped_reportes[asunto] = []
        grouped_reportes[asunto].append(reporte)
    
    # Sort the grouped_reportes by the prioridad of the first reporte in each group (descending order)
    sorted_grouped_reportes = OrderedDict(
        sorted(grouped_reportes.items(), key=lambda item: item[1][0].prioridad or 0)
    )
    
    return render(request, 'reporte/reportes.html', {'reportes_grouped': sorted_grouped_reportes})
