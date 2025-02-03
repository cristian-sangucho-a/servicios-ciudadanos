from django.shortcuts import render, get_object_or_404
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def editar_evento(request, evento_id):
    evento = EventoMunicipal.objects.get(id=evento_id)
    return render(request, 'entidad/eventos/editar_evento.html',{'evento': evento})