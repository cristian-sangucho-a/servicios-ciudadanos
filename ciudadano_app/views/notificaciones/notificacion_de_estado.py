from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from ...decorators import ciudadano_required
from ciudadano_app.models import Ciudadano
from shared.models import Sector, Reporte, TipoReporte, Notificacion

@ciudadano_required
def listar_notificaciones_ciudadano(request):
    ciudadano = request.user
    notificaciones = Notificacion.objects.filter(ciudadano=ciudadano).order_by('-fecha')
    return render(request, 'notificaciones/ver_estado_sector.html', {'notificaciones': notificaciones})

@ciudadano_required
def notificar_reporte_alta_prioridad_ciudadano(request, reporte_id):
    try:
        reporte = Reporte.objects.get(id=reporte_id)
        if reporte.estado != 'Resuelto':
            for ciudadano in Ciudadano.objects.filter(sectores_de_interes__nombre=reporte.ubicacion):
                Notificacion.objects.create(
                    ciudadano=ciudadano,
                    mensaje=f"Nuevo reporte de alta prioridad en {reporte.ubicacion}: {reporte.tipo_reporte.asunto}"
                )
                send_mail(
                    'Reporte de Alta Prioridad',
                    f"Detalles del reporte: {reporte.tipo_reporte.asunto} en {reporte.ubicacion}.",
                    settings.EMAIL_HOST_USER,
                    [ciudadano.correo_electronico],
                    fail_silently=False,
                )
        return redirect('detalle_reporte', reporte_id=reporte.id)
    except ObjectDoesNotExist:
        messages.error(request, 'El reporte no existe.')
        return redirect('lista_reportes')

@ciudadano_required
def notificar_estado_riesgo_ciudadano(request, sector_id):
    try:
        sector = Sector.objects.get(id=sector_id)
        if Reporte.objects.filter(ubicacion=sector.nombre, tipo_reporte__asunto='Robo').count() >= 5:
            sector.estado = 'RIESGO'
            sector.save()
            for ciudadano in Ciudadano.objects.filter(sectores_de_interes__nombre=sector.nombre):
                Notificacion.objects.create(
                    ciudadano=ciudadano,
                    mensaje=f"Precaución: el sector {sector.nombre} ha sido catalogado como de riesgo."
                )
                send_mail(
                    'Sector en Riesgo',
                    f"El sector {sector.nombre} ha sido catalogado como de riesgo.",
                    settings.EMAIL_HOST_USER,
                    [ciudadano.correo_electronico],
                    fail_silently=False,
                )
        return redirect('detalle_sector', sector_id=sector.id)
    except ObjectDoesNotExist:
        messages.error(request, 'El sector no existe.')
        return redirect('lista_sectores')