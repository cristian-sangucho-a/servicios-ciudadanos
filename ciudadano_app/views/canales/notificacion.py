from django.shortcuts import render, redirect
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from shared.models.notificacion.notificacion import Notificacion


def listar_notificacion(request):
    ciudadano = Ciudadano.objects.get(id=request.user.id)
    notificaciones = Notificacion.objects.filter(ciudadano=ciudadano)
    return render(request, 'canales/notificaciones.html', {'notificaciones': notificaciones})
