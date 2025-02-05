from django.shortcuts import render
from ...decorators import ciudadano_required

@ciudadano_required
def listar_sectores_ciudadano(request):
    ciudadano = request.user
    sectores_agregados = ciudadano.sectores_de_interes.all()
    return render(request, 'notificaciones/listar_sectores.html', {
        'sectores_agregados': sectores_agregados
    })