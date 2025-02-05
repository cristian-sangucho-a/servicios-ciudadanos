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
    """
    Según la categoría, se obtienen los eventos:
      - 'mis': Eventos en los que el ciudadano ya está inscrito.
      - 'disponibles': Eventos disponibles para inscripción.
      - 'todos': Eventos próximos (por defecto).
    """
    if categoria == 'mis':
        return EventoMunicipal.objects.para_ciudadano(ciudadano)
    elif categoria == 'disponibles':
        return EventoMunicipal.objects.disponibles_para_inscripcion(ciudadano)
    return EventoMunicipal.objects.proximos()

def preparar_contexto_eventos(eventos, ciudadano):
    """
    Agrega al objeto evento una propiedad 'is_subscribed' que indica si el ciudadano
    ya está inscrito o en lista de espera para ese evento.
    """
    eventos_preparados = []
    for evento in eventos:
        evento.is_subscribed = False
        if ciudadano.is_authenticated:
            evento.is_subscribed = evento.registroasistencia_set.filter(
                ciudadano=ciudadano,
                estado_registro__in=[EstadoRegistro.INSCRITO.value, EstadoRegistro.EN_ESPERA.value]
            ).exists()
        eventos_preparados.append(evento)
    return eventos_preparados

@ciudadano_required
def lista_eventos(request):
    """
    Vista para listar los eventos según la categoría:
      - todos (próximos)
      - mis eventos (inscritos)
      - disponibles (para inscripción)
    """
    categoria = get_categoria_actual(request)
    ciudadano = request.user

    try:
        eventos = obtener_eventos_para_categoria(categoria, ciudadano)
        eventos_preparados = preparar_contexto_eventos(eventos, ciudadano)

        context = {
            'eventos': eventos_preparados,
            'categoria_actual': categoria,
            'total_eventos': EventoMunicipal.objects.proximos().count(),
            'mis_eventos': RegistroAsistencia.objects.filter(
                ciudadano=ciudadano,
                estado_registro__in=[EstadoRegistro.INSCRITO.value, EstadoRegistro.EN_ESPERA.value]
            ).count(),
            'eventos_disponibles': EventoMunicipal.objects.disponibles_para_inscripcion(ciudadano).count(),
        }
        return render(request, 'eventos/lista_eventos.html', context)
    except Exception as e:
        messages.error(request, f"Error al cargar eventos: {str(e)}")
        return redirect('bienvenida_ciudadano')

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
    """
    try:
        registro = RegistroAsistencia.objects.get(
            evento_id=evento_id,
            ciudadano=request.user,
            estado_registro__in=[EstadoRegistro.INSCRITO.value, EstadoRegistro.EN_ESPERA.value]
        )
        registro.cancelar()
        messages.success(request, "Inscripción cancelada correctamente.")
    except RegistroAsistencia.DoesNotExist:
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
        RegistroAsistencia.objects.create(
            ciudadano=request.user,
            evento=evento,
            estado_registro=EstadoRegistro.EN_ESPERA.value
        )
        messages.success(request, "Agregado a lista de espera.")
    except Exception as e:
        messages.error(request, f"Error al agregar a la lista de espera: {str(e)}")
    return redirect('lista_eventos')
