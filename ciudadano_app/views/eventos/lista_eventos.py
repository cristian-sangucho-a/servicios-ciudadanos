from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, F
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia
from entidad_municipal_app.models.evento.enums import EstadoRegistro, EstadoEvento
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ...decorators import ciudadano_required

def get_categoria_actual(request):
    """
    Obtiene la categoría a filtrar de la URL. Por defecto, se muestran todos los eventos.
    """
    return request.GET.get('categoria', 'todos')

def obtener_eventos_para_categoria(categoria, ciudadano):
    """Obtiene los eventos según la categoría seleccionada"""
    if categoria == 'mis' and ciudadano.is_authenticated:
        return EventoMunicipal.objects.mis_eventos(ciudadano)
    return EventoMunicipal.objects.todos_eventos(ciudadano)

def preparar_contexto_eventos(eventos, ciudadano):
    """
    Agrega al objeto evento las propiedades necesarias para la vista
    """
    eventos_preparados = []
    for evento in eventos:
        # Propiedades base
        evento.is_subscribed = False
        evento.estado_registro = None
        
        if ciudadano.is_authenticated:
            # Obtener el registro activo del ciudadano
            registro = evento.registroasistencia_set.filter(
                ciudadano=ciudadano,
                estado_registro__in=[
                    EstadoRegistro.INSCRITO.value,
                    EstadoRegistro.EN_ESPERA.value
                ]
            ).first()
            
            if registro:
                evento.is_subscribed = True
                evento.estado_registro = registro.estado_registro
        
        # Calcular disponibilidad y estado del evento
        ahora = timezone.now()
        es_futuro = evento.fecha_realizacion >= ahora
        esta_programado = evento.estado_actual == EstadoEvento.PROGRAMADO.value
        
        # Asignar propiedades calculadas
        evento.disponible_inscripcion = es_futuro and esta_programado
        evento.es_proximo_temp = es_futuro and esta_programado  # Atributo temporal sin guion bajo
        
        eventos_preparados.append(evento)
    return eventos_preparados

@ciudadano_required
def lista_eventos(request):
    """Vista para listar eventos municipales"""
    categoria = request.GET.get('categoria', 'todos')
    eventos = obtener_eventos_para_categoria(categoria, request.user)
    eventos = preparar_contexto_eventos(eventos, request.user)
    
    # Preparar contadores
    total_eventos = EventoMunicipal.objects.filter(
        estado_actual=EstadoEvento.PROGRAMADO.value,
        fecha_realizacion__gte=timezone.now()
    ).count()
    
    mis_eventos = 0
    if request.user.is_authenticated:
        mis_eventos = EventoMunicipal.objects.filter(
            registroasistencia_set__ciudadano=request.user,
            registroasistencia_set__estado_registro__in=[
                EstadoRegistro.INSCRITO.value,
                EstadoRegistro.EN_ESPERA.value
            ]
        ).distinct().count()
    
    context = {
        'eventos': eventos,
        'categoria_actual': categoria,
        'total_eventos': total_eventos,
        'mis_eventos': mis_eventos,
    }
    
    return render(request, 'eventos/lista_eventos.html', context)

@ciudadano_required
def inscribirse_evento(request, evento_id):
    """
    Vista para inscribir al ciudadano en el evento.
    """
    try:
        evento = get_object_or_404(EventoMunicipal, pk=evento_id)
        evento.inscribir_ciudadano(request.user)
        messages.success(request, "Inscripción realizada correctamente.")
    except Exception as e:
        messages.error(request, f"Error al inscribir: {str(e)}")
    return redirect('lista_eventos')

@ciudadano_required
def cancelar_inscripcion(request, evento_id):
    """
    Vista para cancelar la inscripción del ciudadano en el evento.
    Si el ciudadano estaba inscrito, se promoverá automáticamente al siguiente en lista de espera.
    """
    try:
        evento = get_object_or_404(EventoMunicipal, pk=evento_id)
        registro = evento.obtener_registro_activo(request.user)
        if registro:
            registro_cancelado, registro_promovido = evento.cancelar_inscripcion(registro.pk)
            messages.success(request, "Inscripción cancelada correctamente.")
            if registro_promovido:
                messages.info(request, "Se ha promovido al siguiente ciudadano de la lista de espera.")
        else:
            messages.error(request, "No se encontró una inscripción activa para cancelar.")
    except Exception as e:
        messages.error(request, f"Error al cancelar la inscripción: {str(e)}")
    return redirect('lista_eventos')

@ciudadano_required
def lista_espera_evento(request, evento_id):
    """
    Vista para agregar al ciudadano a la lista de espera de un evento.
    """
    try:
        evento = get_object_or_404(EventoMunicipal, pk=evento_id)
        evento.agregar_a_lista_espera(request.user)
        messages.success(request, "Agregado a lista de espera.")
    except Exception as e:
        messages.error(request, f"Error al agregar a la lista de espera: {str(e)}")
    return redirect('lista_eventos')
