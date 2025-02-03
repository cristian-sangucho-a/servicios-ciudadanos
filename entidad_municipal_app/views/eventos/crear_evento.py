from django.shortcuts import render, redirect
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required


@entidad_required
@login_required
def crear_evento(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre_evento = request.POST.get('nombre_evento')
        descripcion_evento = request.POST.get('descripcion_evento')
        fecha_realizacion = request.POST.get('fecha_realizacion')
        lugar_evento = request.POST.get('lugar_evento')
        capacidad_maxima = request.POST.get('capacidad_maxima')

        # Obtener la entidad municipal del usuario autenticado
        entidad_municipal = request.user  # Asegúrate de que esto sea correcto

        # Crear el evento usando el manager
        try:
            EventoMunicipal.objects.create_evento_con_aforo(
                nombre=nombre_evento,
                descripcion=descripcion_evento,
                fecha=fecha_realizacion,
                lugar=lugar_evento,
                capacidad=capacidad_maxima,
                entidad_municipal=entidad_municipal
            )
            # Redirigir a la página de gestión de eventos
            return redirect('gestor_eventos')
        except Exception as e:
            # Manejo de errores, puedes agregar un mensaje de error aquí
            print(f"Error al crear el evento: {e}")

    return render(request, 'entidad/eventos/crear_evento.html')