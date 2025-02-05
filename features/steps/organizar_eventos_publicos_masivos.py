from behave import step
from faker import Faker
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.enums import EstadoEvento, EstadoEspacioPublico
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from entidad_municipal_app.models.evento.gestor_eventos import RepositorioEventos
from mocks.repositorio_eventos_memoria import (
    crear_entidad_municipal_aleatoria,
    crear_espacio_publico_aleatorio,
    crear_evento_aleatorio, crear_ciudadano_aleatorio
)
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

repositorio = RepositorioEventos()

fake = Faker()

@step("que una entidad municipal desea organizar un evento")
def step_impl(context):
    """Crea una entidad municipal aleatoria"""
    context.entidad_municipal = crear_entidad_municipal_aleatoria()
    context.evento = None

@step('la fecha del evento es "{fecha_evento}"')
def step_impl(context, fecha_evento):
    """Guarda la fecha del evento en el contexto"""
    context.fecha_realizacion = datetime.strptime(fecha_evento, "%Y-%m-%d %H:%M:%S")

@step('el espacio público "{nombre_espacio_publico}" se encuentre en estado {estado_espacio_publico}')
def step_impl(context, nombre_espacio_publico, estado_espacio_publico):
    """Crea un espacio público aleatorio con el estado especificado"""
    # Convertir el string del estado a enum value
    estado = EstadoEspacioPublico[estado_espacio_publico].value
    context.espacio_publico = crear_espacio_publico_aleatorio(
        nombre_espacio_publico,
        estado,
        context.entidad_municipal
    )
    context.disponible = context.espacio_publico.estado_espacio_publico == EstadoEspacioPublico.DISPONIBLE.value
    if not context.disponible:
        print(f"El espacio '{context.espacio_publico.nombre}' no está disponible para eventos.")

@step("se creara el evento")
def step_impl(context):
    """Crea un evento si el espacio público está disponible"""
    if context.disponible:
        context.evento = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Concierto de Música",
            descripcion="Un concierto al aire libre con artistas locales.",
            fecha=context.fecha_realizacion,
            lugar=context.espacio_publico.nombre,
            capacidad=500,
            entidad_municipal=context.entidad_municipal,
            espacio_publico=context.espacio_publico
        )

@step("cambiara el estado del espacio público")
def step_impl(context):
    """Cambia el estado del espacio público a NO DISPONIBLE"""
    context.espacio_publico.estado_espacio_publico = EstadoEspacioPublico.NO_DISPONIBLE.value
    context.espacio_publico.save()

@step('el espacio público "{nombre_espacio_publico}" se encuentra en estado {estado_espacio_publico}')
def step_impl(context, nombre_espacio_publico, estado_espacio_publico):
    """Crea un espacio público aleatorio con el estado especificado"""
    estado = EstadoEspacioPublico[estado_espacio_publico].value
    context.espacio_publico = crear_espacio_publico_aleatorio(
        nombre_espacio_publico,
        estado,
        context.entidad_municipal
    )

@step("no se creara el evento")
def step_impl(context):
    """Verifica si el espacio público está disponible"""
    if context.espacio_publico.estado_espacio_publico == EstadoEspacioPublico.NO_DISPONIBLE.value:
        print("El espacio público no está disponible para este evento.")
        assert context.evento is None, "Se esperaba que el evento no se creara."
    else:
        raise AssertionError(
            f"Se esperaba que el espacio '{context.espacio_publico.nombre}' no estuviera disponible, pero está disponible.")

@step("se mostrarán los espacios públicos disponibles")
def step_impl(context):
    """Obtenemos los espacios disponibles sin necesidad de filtrar por fecha"""
    espacios_disponibles = EspacioPublico.obtener_espacios_disponibles(filtrar_disponibles=True)
    if espacios_disponibles.exists():
        print("Espacios públicos disponibles:")
        for espacio in espacios_disponibles:
            print(f"{espacio.nombre} - {espacio.direccion}")
    else:
        print("No hay espacios públicos disponibles.")

@step('que existe un evento llamado "{nombre_evento}" con el estado "{estado_evento}"')
def step_existe_evento(context, nombre_evento, estado_evento):
    """Se guardan los datos para crear el evento en pasos siguientes"""
    if estado_evento == "NULL":
        context.evento = None
        return
        
    context.nombre_evento = nombre_evento
    context.estado_evento = EstadoEvento[estado_evento].value

@step('el espacio público destinado al evento es "{nombre_espacio}"')
def step_asigna_espacio(context, nombre_espacio):
    """Asigna un espacio público al evento con los datos anteriores"""
    if nombre_espacio == "NULL":
        context.espacio_publico = None
        return
        
    context.entidad_municipal = crear_entidad_municipal_aleatoria()
    context.espacio_publico = crear_espacio_publico_aleatorio(
        nombre_espacio=nombre_espacio,
        estado=EstadoEspacioPublico.DISPONIBLE.value,
        entidad_municipal=context.entidad_municipal
    )

    context.evento = EventoMunicipal.objects.crear_evento_con_aforo(
        nombre=context.nombre_evento,
        descripcion=fake.paragraph(),
        fecha=timezone.now() + timedelta(days=7),
        lugar=nombre_espacio,
        capacidad=18,
        entidad_municipal=context.entidad_municipal,
        espacio_publico=context.espacio_publico,
    )

@step('el espacio publico esta en situación de "{estado_espacio}" debido a un "{motivo_riesgo}"')
def step_cambia_estado_espacio(context, estado_espacio, motivo_riesgo):
    """Cambia el estado del espacio público y registra el motivo de riesgo."""
    if estado_espacio == "NULL" or motivo_riesgo == "NULL":
        return
        
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
    """Cambia el estado del evento usando el repositorio."""
    if nuevo_estado_evento == "NULL":
        return
        
    try:
        if nuevo_estado_evento == EstadoEvento.CANCELADO.value:
            if hasattr(context, "motivo_riesgo"):
                repositorio.cancelar_evento(context.evento.id, context.motivo_riesgo)
            else:
                print("No se puede cancelar sin un motivo de riesgo.")
    except Exception as e:
        print(f"No se pudo cambiar el estado del evento: {e}")

@step('se registra el motivo de la cancelación')
def step_registra_motivo_cancelacion(context):
    """Registra el motivo de la cancelación si el evento está cancelado."""
    if context.evento is None:
        print("No existe evento para registrar motivo de cancelación.")
        return

    if context.evento.estado_actual == EstadoEvento.CANCELADO.value:
        if hasattr(context, "motivo_riesgo"):
            context.evento.set_motivo_cancelacion(context.motivo_riesgo)
            context.evento.save()
            print(f"Motivo de cancelación registrado: {context.motivo_riesgo}")
        else:
            print("No se encontró motivo de cancelación.")


@step('se cumple el minimo de {capacidad_minima} cuidadanos para crear el evento')
def step_impl(context,capacidad_minima):
    context.ciudadano = crear_ciudadano_aleatorio()
    context.evento = EventoMunicipal.inscribir_ciudadano( context.ciudadano)


@step("se actualizara el estado del evento")
def step_impl(context):
   context.evento = context.evento.actualizar_estado_evento(context.evento)








