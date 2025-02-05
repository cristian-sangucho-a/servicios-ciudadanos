from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.enums import EstadoEvento, EstadoRegistro
from entidad_municipal_app.decorators import entidad_required

@entidad_required
@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(EventoMunicipal, id=evento_id)
    
    # No permitir editar eventos cancelados
    if evento.estado_actual == EstadoEvento.CANCELADO.value:
        messages.error(request, 'No se puede editar un evento cancelado.')
        return redirect('gestor_eventos')
    
    try:
        if request.method == 'POST':
            # Validar y parsear la fecha
            fecha_realizacion = request.POST.get('fecha_realizacion')
            try:
                fecha_datetime = datetime.strptime(fecha_realizacion, "%Y-%m-%dT%H:%M")
                if fecha_datetime < timezone.now():
                    if evento.estado_actual == EstadoEvento.PROGRAMADO.value:
                        messages.error(request, "No se puede programar un evento para una fecha pasada.")
                        return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})
            except ValueError:
                messages.error(request, "Formato de fecha no válido. Usa el formato correcto (YYYY-MM-DDTHH:MM).")
                return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})
            
            # Validar y convertir la capacidad
            capacidad_maxima = request.POST.get('capacidad_maxima')
            try:
                nueva_capacidad = int(capacidad_maxima)
                if nueva_capacidad <= 0:
                    raise ValueError("La capacidad debe ser mayor a 0")
                    
                # Verificar que la nueva capacidad no sea menor que los inscritos actuales
                inscritos_actuales = evento.registroasistencia_set.filter(
                    estado_registro=EstadoRegistro.INSCRITO.value
                ).count()
                
                if nueva_capacidad < inscritos_actuales:
                    messages.error(request, 
                        f'La capacidad no puede ser menor que el número de inscritos actuales ({inscritos_actuales}).')
                    return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})
                    
                evento.capacidad_maxima = nueva_capacidad
            except ValueError as e:
                messages.error(request, f'Error en la capacidad máxima: {str(e)}')
                return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})
            
            # Actualizar campos básicos
            evento.nombre_evento = request.POST.get('nombre_evento')
            evento.descripcion_evento = request.POST.get('descripcion_evento')
            evento.fecha_realizacion = fecha_datetime
            
            # Validar todos los campos antes de guardar
            try:
                evento.full_clean()
                evento.save()
                messages.success(request, 'El evento se ha editado exitosamente.')
                return redirect('gestor_eventos')
            except ValidationError as e:
                messages.error(request, f'Error de validación: {str(e)}')
                return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})
                
    except Exception as e:
        messages.error(request, f'Error al editar el evento: {str(e)}')

    return render(request, 'entidad/eventos/editar_evento.html', {'evento': evento})