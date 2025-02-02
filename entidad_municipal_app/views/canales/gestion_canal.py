from django.shortcuts import render, redirect
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo

def listar_canales_administrados(request):
    #TODO: CAMBIAR POR LA ENTIDAD MUNICIPAL QUE SE RECIBA EN EL REQUEST
    entidad_municipal = EntidadMunicipal.objects.get(id = 2)
    canales = CanalInformativo.objects.filter(entidad_municipal = entidad_municipal)
    return render(request, 'canales/lista_canales_administrados.html',{'canales':canales})

def crear_canal_form(request):
    return render(request, 'canales/crear_canal.html')

def crear_canal(request):
    if request.method == 'POST':
        # TODO: CAMBIAR POR LA ENTIDAD MUNICIPAL QUE SE RECIBA EN EL REQUEST
        entidad_municipal = EntidadMunicipal.objects.get(id=2)
        nombre = request.POST.get('nombre_canal')
        descripcion = request.POST.get('descripcion_canal')
        es_emergencia = request.POST.get('es_emergencia')
        if nombre and descripcion and es_emergencia:
            CanalInformativo.objects.create(
                entidad_municipal=entidad_municipal,
                nombre=nombre,
                descripcion=descripcion,
                es_emergencia=es_emergencia
            )
            canal = CanalInformativo.objects.get(nombre=nombre)
            if canal.es_emergencia:
                ciudadanos = Ciudadano.objects.all()
                for ciudadano in ciudadanos:
                    canal.suscribir_ciudadano(ciudadano)
    return redirect("/entidad_municipal/lista_canales/")

def eliminar_canal(request,canal_id):
    canal= CanalInformativo.objects.get(id=canal_id)
    canal.delete()
    return redirect("/entidad_municipal/lista_canales/")