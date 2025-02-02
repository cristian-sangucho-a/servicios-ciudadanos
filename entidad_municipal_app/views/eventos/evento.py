from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia, EstadoRegistroAsistencia
from entidad_municipal_app.decorators import entidad_required

@entidad_required
def evento(request, evento_id):
    """Vista para mostrar el detalle de un evento y sus inscritos."""
    try:
        # Obtener el evento
        evento = get_object_or_404(EventoMunicipal, id=evento_id)
        print(f"Evento encontrado: {evento.nombre_evento}")  # Debug
        
        # Obtener todos los registros de asistencia para depuración
        todos_registros = RegistroAsistencia.objects.filter(evento=evento)
        print(f"Total de registros encontrados: {todos_registros.count()}")
        for registro in todos_registros:
            print(f"Registro: {registro.ciudadano.nombre_completo} - Estado: {registro.estado_registro}")
        
        # Obtener los registros de asistencia (inscritos)
        inscritos = RegistroAsistencia.objects.filter(
            evento=evento,
            estado_registro=EstadoRegistroAsistencia.INSCRITO  # Filtramos solo los inscritos
        ).select_related('ciudadano').order_by('fecha_inscripcion')
        
        print(f"Inscritos encontrados: {inscritos.count()}")  # Debug
        for inscrito in inscritos:
            print(f"Inscrito: {inscrito.ciudadano.nombre_completo}")
        
        # Renderizar el template
        context = {
            'evento': evento,
            'inscritos': inscritos
        }
        return render(request, 'entidad/eventos/evento.html', context)
    
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug
        raise