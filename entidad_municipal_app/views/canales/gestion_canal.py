from django.shortcuts import render

from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo

def listar_canales_administrados(request):
    entidad_municipal = EntidadMunicipal.objects.get(id=request.user.id)
    canales = CanalInformativo.objects.filter(entidad_municipal=entidad_municipal)
    return render(request, 'canales/lista_canales.html',canales)