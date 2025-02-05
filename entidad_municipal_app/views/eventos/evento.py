from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia
from entidad_municipal_app.decorators import entidad_required

@entidad_required
@require_http_methods(["GET"])
def evento(request, evento_id):
    """
    Vista que muestra el detalle del evento, incluyendo la tabla de ciudadanos registrados
    y sus estados de asistencia.
    """
    evento_obj = get_object_or_404(EventoMunicipal, pk=evento_id)
    inscritos = evento_obj.registroasistencia_set.all()
    
    context = {
        'evento': evento_obj,
        'inscritos': inscritos,
    }
    return render(request, 'entidad/eventos/evento.html', context)

@entidad_required
@require_http_methods(["POST"])
def actualizar_asistencia(request, registro_id):
    """
    Vista que procesa la actualización de la asistencia de un ciudadano a un evento.
    Se espera que el formulario envíe un campo 'nuevo_estado' con el valor 'ASISTIO' o 'NO_ASISTIO'.
    """
    if request.method == 'POST':
        registro = get_object_or_404(RegistroAsistencia, pk=registro_id)
        nuevo_estado = request.POST.get('nuevo_estado')
        
        # Validamos que se haya enviado un valor correcto
        if nuevo_estado not in ['ASISTIO', 'NO_ASISTIO']:
            messages.error(request, "Estado de asistencia inválido.")
            return redirect('detalle_evento', evento_id=registro.evento.pk)
        
        # Convertimos el valor a un booleano para el método marcar_asistencia
        asistio = nuevo_estado == 'ASISTIO'
        
        try:
            # El método marcar_asistencia se encarga de verificar que el evento esté en curso
            registro.evento.marcar_asistencia(registro_id, asistio)
            messages.success(request, "La asistencia se ha actualizado correctamente.")
        except Exception as e:
            messages.error(request, f"Error al actualizar la asistencia: {str(e)}")
        
        return redirect('detalle_evento', evento_id=registro.evento.pk)
    
    return redirect('detalle_evento', evento_id=registro.evento.pk)

@entidad_required
@require_http_methods(["POST"])
def eliminar_inscripcion(request, registro_id):
    """
    Vista que permite eliminar la inscripción de un ciudadano a un evento.
    Si el ciudadano estaba inscrito, se promoverá automáticamente al siguiente en lista de espera.
    """    
    # Obtenemos el registro y el evento antes de cualquier operación
    registro = get_object_or_404(RegistroAsistencia, pk=registro_id)
    evento_id = registro.evento.pk  # Guardamos el ID del evento
    evento = registro.evento
    
    try:
        registro_cancelado, registro_promovido = evento.cancelar_inscripcion(registro_id)
        
        messages.success(request, "La inscripción ha sido eliminada correctamente.")
        if registro_promovido:
            messages.info(request, "Se ha promovido al siguiente ciudadano de la lista de espera.")
    except Exception as e:
        messages.error(request, f"Error al eliminar la inscripción: {str(e)}")
    
    return redirect('detalle_evento', evento_id=evento_id)  # Usamos el ID guardado