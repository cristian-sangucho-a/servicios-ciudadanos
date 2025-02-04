from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from entidad_municipal_app.decorators import entidad_required
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.espacio_publico import EspacioPublico

@entidad_required
@login_required
def crear_evento(request):
    # Obtener parámetros de búsqueda y filtro
    query = request.GET.get('q')  # Término de búsqueda
    filtrar_disponibles = request.GET.get('disponibles', False)  # Filtro de disponibilidad

    # Llamar al método para obtener los espacios disponibles
    espacios = EspacioPublico.obtener_espacios_disponibles(query=query, filtrar_disponibles=filtrar_disponibles)

    # Procesar el formulario cuando se envía
    if request.method == 'POST':
        nombre_evento = request.POST.get('nombre_evento')
        descripcion_evento = request.POST.get('descripcion_evento')
        fecha_realizacion = request.POST.get('fecha_realizacion')
        espacio_publico_id = request.POST.get('espacio_publico')
        capacidad_maxima = request.POST.get('capacidad_maxima')
        entidad_municipal = request.user

        try:
            # Verificar si el espacio seleccionado está disponible
            espacio_publico = EspacioPublico.objects.get(pk=espacio_publico_id)
            espacio_publico.estado_incidente_espacio = EspacioPublico.NO_AFECTADO
            if espacio_publico.estado_espacio_publico != EspacioPublico.ESTADO_DISPONIBLE:
                espacios = EspacioPublico.obtener_espacios_disponibles(query=query,filtrar_disponibles=True)
                messages.error(request, 'El espacio seleccionado no está disponible. Selecciona un espacio disponible.')
                return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios})

            # Crear el evento
            EventoMunicipal.objects.crear_evento_con_aforo(
                nombre=nombre_evento,
                descripcion=descripcion_evento,
                fecha=fecha_realizacion,
                lugar=espacio_publico.direccion,
                capacidad=capacidad_maxima,
                entidad_municipal=entidad_municipal,
                espacio_publico=espacio_publico
            )
            messages.success(request, 'El evento se ha creado exitosamente.')
            return redirect('gestor_eventos')
        except Exception as e:
            messages.error(request, f'Error al crear el evento: {str(e)}')

    return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios, 'query': query, 'disponibles': filtrar_disponibles})