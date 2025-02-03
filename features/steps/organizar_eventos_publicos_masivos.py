from behave import step
from faker import Faker
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from entidad_municipal_app.models.evento.gestor_eventos import RepositorioEventos
from mocks.repositorio_eventos_memoria import (
    crear_entidad_municipal_aleatoria,
    crear_espacio_publico_aleatorio,
    crear_evento_aleatorio
)
repositorio = RepositorioEventos()
# use_step_matcher("re")

fake = Faker()

@step("que una entidad municipal desea organizar un evento")
def step_impl(context):
    """Crea una entidad municipal aleatoria"""
    context.entidad_municipal = crear_entidad_municipal_aleatoria()
    context.evento = None

@step('la fecha del evento es {fecha_evento}')
def step_impl(context, fecha_evento):
    """Guarda la fecha del evento en el contexto"""
    context.fecha_realizacion = fake.date_time().strftime("%Y-%m-%d %H:%M:%S")


@step('el espacio público {nombre_espacio_publico} se encuentre en estado {estado_espacio_publico}')
def step_impl(context, nombre_espacio_publico, estado_espacio_publico):
    """Crea un espacio público aleatorio con el estado especificado"""
    context.estado_disponible = estado_espacio_publico
    context.espacio_publico = crear_espacio_publico_aleatorio(nombre_espacio_publico,context.estado_disponible,context.entidad_municipal)


@step("se creara el evento")
def step_impl(context):
    """Crea un evento si el espacio público está disponible"""
    if context.espacio_publico.estado_espacio_publico == EspacioPublico.ESTADO_DISPONIBLE:
        context.evento = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Concierto de Música",
            descripcion="Un concierto al aire libre con artistas locales.",
            fecha=timezone.now() + timezone.timedelta(days=7),
            lugar="Parque Central",
            capacidad=500,
            entidad_municipal=context.entidad_municipal,
            espacio_publico=context.espacio_publico
        )

@step("cambiara el estado del espacio público")
def step_impl(context):
    """Cambia el estado del espacio público a NO DISPONIBLE"""
    context.espacio_publico.estado_espacio_publico = EspacioPublico.ESTADO_NO_DISPONIBLE

@step('el espacio público "{nombre_espacio_publico}" se encuentra en estado {estado_espacio_publico}')
def step_impl(context, nombre_espacio_publico, estado_espacio_publico):
    """Crea un espacio público aleatorio con el estado especificado"""
    context.estado_no_disponible = estado_espacio_publico
    context.espacio_publico = crear_espacio_publico_aleatorio(nombre_espacio_publico,context.estado_no_disponible,context.entidad_municipal)


@step("no se creara el evento")
def step_impl(context):
    """Verifica si el espacio público está disponible"""
    if context.espacio_publico.estado_espacio_publico == EspacioPublico.ESTADO_NO_DISPONIBLE:
        print("El espacio público no está disponible para este evento.")
        """Asegura que el evento no se haya creado"""
        assert context.evento is None, "Se esperaba que el evento no se creara."
    else:
        """Si el espacio público está disponible, esto es un caso inesperado"""
        raise AssertionError(
            f"Se esperaba que el espacio '{context.espacio_publico.nombre}' no estuviera disponible, pero está disponible.")

@step("se mostrarán los espacios públicos disponibles")
def step_impl(context):
    """obtenemos los espacios disponibles"""
    espacios_disponibles = EspacioPublico.obtener_espacios_disponibles(context.fecha_realizacion)
    """mostramos los espacios públicos disponibles"""
    if espacios_disponibles.exists():
        print("Espacios públicos disponibles:")
        for espacio in espacios_disponibles:
            print(f"{espacio.nombre} - {espacio.direccion}")
    else:
        print("No hay espacios públicos disponibles.")


@step('que existe un evento llamado "{nombre_evento}" con el estado "{estado_evento}"')
def step_existe_evento(context, nombre_evento, estado_evento):
    """
    Se guardan los datos para crear el evento en pasos siguientes
    """
    context.nombre_evento = nombre_evento
    context.estado_evento = estado_evento

@step('el espacio público destinado al evento es "{nombre_espacio}"')
def step_asigna_espacio(context, nombre_espacio):
    """
    Asigna un espacio público al evento con los datos anteriores
    """
    #context.espacio_publico = crear_espacio_publico_aleatorio(nombre_espacio=nombre_espacio,estado='DISPONIBLE',entidad_municipal=crear_entidad_municipal_aleatoria())
    context.entidad_municipal = crear_entidad_municipal_aleatoria()
    context.espacio_publico = crear_espacio_publico_aleatorio(nombre_espacio=nombre_espacio,estado= "DISPONIBLE", entidad_municipal=context.entidad_municipal)

    context.evento = EventoMunicipal.objects.crear_evento_con_aforo(
        nombre=context.nombre_evento,
        descripcion=fake.paragraph(),
        fecha=timezone.now() + timedelta(days=7),
        lugar="Parque Central",
        capacidad=18,
        entidad_municipal=context.entidad_municipal,
        espacio_publico=context.espacio_publico,
    )

@step('el espacio publico esta en situación de "{estado_espacio}" debido a un "{motivo_riesgo}"')
def step_cambia_estado_espacio(context, estado_espacio, motivo_riesgo):
    """
    Cambia el estado del espacio público y registra el motivo de riesgo.
    """
    context.estado_espacio = estado_espacio
    context.motivo_riesgo = motivo_riesgo

    if context.evento is None:
        print("No existe evento a cancelar.")
        return

    try:
        if estado_espacio and context.evento.espacio_publico:
            context.evento.espacio_publico.estado_incidente_espacio = estado_espacio
            context.evento.espacio_publico.save()
            print("Estado guardado", context.evento.espacio_publico.estado_incidente_espacio)
    except Exception as e:
        print(f"No se pudo cambiar el estado del lugar: {e}")


@step('la entidad municipal cambia el estado del evento a "{nuevo_estado_evento}"')
def step_cambia_estado_evento(context, nuevo_estado_evento):
    """
    Cambia el estado del evento usando el repositorio.
    """
    try:
        if nuevo_estado_evento == EventoMunicipal.ESTADO_CANCELADO:
            if hasattr(context, "motivo_riesgo"):
                repositorio.cancelar_evento(context.evento.id, context.motivo_riesgo)
            else:
                print("No se puede cancelar sin un motivo de riesgo.")
    except Exception as e:
        print(f"No se pudo cambiar el estado del evento: {e}")

@step('se registra el motivo de la cancelación')
def step_registra_motivo_cancelacion(context):
    """
    Registra el motivo de la cancelación si el evento está cancelado.
    """
    if context.evento is None:
        print("No existe evento para registrar motivo de cancelación.")
        return

    if context.evento.estado_actual == EventoMunicipal.ESTADO_CANCELADO:
        if hasattr(context, "motivo_riesgo"):
            context.evento.set_motivo_cancelacion(context.motivo_riesgo)
            context.evento.save()
            print(f"Motivo de cancelación registrado: {context.motivo_riesgo}")
        else:
            print("No se encontró motivo de cancelación.")
