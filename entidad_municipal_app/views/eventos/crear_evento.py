from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from entidad_municipal_app.decorators import entidad_required
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.espacio_publico import EspacioPublico
from entidad_municipal_app.models.evento.enums import EstadoEvento, EstadoEspacioPublico

@entidad_required
@login_required
def crear_evento(request):
    # Parámetros de búsqueda y filtro
    query = request.GET.get('q')
    filtrar_disponibles = request.GET.get('disponibles', False)

    # Obtener los espacios disponibles
    espacios = EspacioPublico.obtener_espacios_disponibles(query=query, filtrar_disponibles=filtrar_disponibles)

    if request.method == 'POST':
        nombre_evento = request.POST.get('nombre_evento')
        descripcion_evento = request.POST.get('descripcion_evento')
        fecha_realizacion = request.POST.get('fecha_realizacion')
        espacio_publico_id = request.POST.get('espacio_publico')
        capacidad_maxima = request.POST.get('capacidad_maxima')
        entidad_municipal = request.user

        try:
            # Verificar que el espacio exista y esté disponible
            espacio_publico = EspacioPublico.objects.get(pk=espacio_publico_id)
            
            # Verificar que el espacio no esté afectado
            if espacio_publico.estado_incidente_espacio == EspacioPublico.AFECTADO:
                messages.error(request, 'El espacio público está afectado por un incidente y no puede ser utilizado.')
                return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios})
            
            # Verificar que el espacio esté disponible
            if espacio_publico.estado_espacio_publico != EspacioPublico.ESTADO_DISPONIBLE:
                espacios = EspacioPublico.obtener_espacios_disponibles(query=query, filtrar_disponibles=True)
                messages.error(request, 'El espacio seleccionado no está disponible. Selecciona un espacio disponible.')
                return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios})
            
            # Validar y parsear la fecha
            try:
                fecha_datetime = datetime.strptime(fecha_realizacion, "%Y-%m-%dT%H:%M")
                # Convertir a timezone-aware
                fecha_datetime = timezone.make_aware(fecha_datetime)
                if fecha_datetime < timezone.now():
                    messages.error(request, "No puedes crear un evento en el pasado.")
                    return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios})
            except ValueError:
                messages.error(request, "Formato de fecha no válido. Usa el formato correcto (YYYY-MM-DDTHH:MM).")
                return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios})
            
            # Convertir capacidad a entero
            try:
                capacidad_maxima = int(capacidad_maxima)
                if capacidad_maxima <= 0:
                    raise ValueError("La capacidad debe ser mayor a 0")
            except ValueError as e:
                messages.error(request, f'Error en la capacidad máxima: {str(e)}')
                return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios})
            
            # Crear el evento usando el método del manager que gestiona el aforo
            evento = EventoMunicipal.objects.crear_evento_con_aforo(
                nombre=nombre_evento,
                descripcion=descripcion_evento,
                fecha=fecha_datetime,
                lugar=espacio_publico.direccion,
                capacidad=capacidad_maxima,
                entidad_municipal=entidad_municipal,
                espacio_publico=espacio_publico
            )
            
            # Marcar el espacio como no disponible
            espacio_publico.marcar_como_no_disponible()
            
            messages.success(request, 'El evento se ha creado exitosamente.')
            return redirect('gestor_eventos')
            
        except ValidationError as e:
            messages.error(request, f'Error de validación: {str(e)}')
        except Exception as e:
            messages.error(request, f'Error al crear el evento: {str(e)}')

    return render(request, 'entidad/eventos/crear_evento.html', {'espacios': espacios, 'query': query, 'disponibles': filtrar_disponibles})