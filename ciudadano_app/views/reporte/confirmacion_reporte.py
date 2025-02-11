from django.shortcuts import render, redirect

from shared.models.reporte.reporte import Reporte
from shared.models.reporte.tipo_reporte import TipoReporte
from ...admin import Ciudadano
from shared.models import ServicioDeReporte, RepositorioDeReporteDjango

repositorioReporte = RepositorioDeReporteDjango()
servicioDeReporte = ServicioDeReporte(repositorioReporte)

def confirmar_reporte(request, reporte_id):
    """Confirmación de un reporte"""
    if request.method == 'POST':
        ciudadano = request.user  # Suponiendo que el usuario está autenticado
        asunto = request.POST.get('asunto')
        ubicacion = request.POST.get('ubicacion')

        # Buscar el reporte original por ID
        reporte_original = Reporte.objects.get(id=reporte_id)

        # Crear el nuevo reporte confirmado
        reporte_confirmado = Reporte(
            ciudadano=ciudadano,
            tipo_reporte=reporte_original.tipo_reporte,  # Usar el tipo del reporte original
            ubicacion=ubicacion
        )

        # Confirmar el reporte y priorizar
        reporte_confirmado = servicioDeReporte.enviar_reporte(reporte=reporte_confirmado)
        servicioDeReporte.priorizar(reporte_confirmado)

        # Redirigir o mostrar mensaje de éxito
        return render(request, 'reporte/envio_reporte.html', {
            'tipo_reportes': TipoReporte.objects.all(),
            'success_message': 'Reporte confirmado y enviado con éxito',
            'asunto': asunto,
            'ubicacion': ubicacion,
            'ciudadano_id': ciudadano.id,
            'descripcion': reporte_original.tipo_reporte.descripcion,
            'auto_send': True
        })
    else:
        # Si el método no es POST, simplemente mostramos el reporte original y el formulario de confirmación
        reporte_original = Reporte.objects.get(id=reporte_id)
        return render(request, 'reporte/envio_reporte.html', {
            'reporte': reporte_original,
            'tipo_reportes': TipoReporte.objects.all()
        })
