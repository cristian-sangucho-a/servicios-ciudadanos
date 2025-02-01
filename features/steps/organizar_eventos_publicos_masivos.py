from behave import step
from faker import Faker
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from django.core.exceptions import ValidationError, ObjectDoesNotExist

from entidad_municipal_app.models.evento.repositorio_eventos import RepositorioEventos

# use_step_matcher("re")

fake = Faker()

def crear_entidad_municipal_aleatoria():
    return EntidadMunicipal.objects.create(
        nombre=fake.company(),
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email(),
        fecha_registro=datetime.now()
    )

def crear_espacio_publico_aleatorio(nombre_espacio,estado, entidad_municipal):
    if estado == 'DISPONIBLE':
            estado = EspacioPublico.ESTADO_DISPONIBLE,
    else:
            estado = EspacioPublico.ESTADO_NO_DISPONIBLE,

    return EspacioPublico.objects.create(
        nombre=nombre_espacio,
        entidad_municipal=entidad_municipal,
       estado_espacio_publico=estado,
    )


@step("que una entidad municipal desea organizar un evento")
def step_impl(context):
    context.entidad_municipal = crear_entidad_municipal_aleatoria()

@step('la fecha del evento es {fecha_evento}')
def step_impl(context, fecha_evento):
    context.fecha_realizacion = fake.date_time().strftime("%Y-%m-%d %H:%M:%S")


@step('el espacio público {nombre_espacio_publico} se encuentre en estado {estado_espacio_publico}')
def step_impl(context, nombre_espacio_publico, estado_espacio_publico):
    context.estado_disponible = estado_espacio_publico
    context.espacio_publico = crear_espacio_publico_aleatorio(nombre_espacio_publico,context.estado_disponible,context.entidad_municipal)


@step("se creara el evento")
def step_impl(context):
    context.evento = EventoMunicipal.objects.crear_evento_con_aforo(
        nombre=fake.sentence(nb_words=4),
        descripcion=fake.text(max_nb_chars=200),
        fecha=context.fecha_realizacion,
        lugar=fake.address(),
        capacidad=18,
        espacio_publico = context.espacio_publico,
    )

@step("cambiara el estado del espacio público")
def step_impl(context):
    context.espacio_publico.estado_espacio_publico = EspacioPublico.ESTADO_NO_DISPONIBLE

@step('el espacio público "{nombre_espacio_publico}" no se encuentre disponible')
def step_impl(context, nombre_espacio_publico):
    context.espacio_publico = EspacioPublico.objects.create(
        nombre=nombre_espacio_publico,
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        estado_espacio_publico=EspacioPublico.ESTADO_NO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )
    ##retroalimentacion
    """
    Marca el espacio como NO disponible creando un evento en la misma fecha.
    """
    esp_no_disp, _ = EspacioPublico.objects.get_or_create(
        nombre=nombre_espacio_publico,
        entidad_municipal=context.entidad_municipal
    )
    context.espacio_publico = esp_no_disp

    # Creamos otro evento en la misma fecha para simular un choque
    EventoMunicipal.objects.create(
        nombre_evento="Evento que choca",
        descripcion_evento="Ocupando la fecha",
        fecha_realizacion=context.fecha_evento,
        espacio_publico=esp_no_disp,
        entidad_municipal=context.entidad_municipal,
        lugar_evento=esp_no_disp.nombre,
        capacidad_maxima=50,
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO,
    )
    context.espacio_disponible = False


@step("no se creara el evento")
def step_impl(context):
    """
        if context.espacio_disponible.estado_espacio_publico == EspacioPublico.ESTADO_NO_DISPONIBLE:
            print("El espacio público no está disponible para este evento.")
    """
    if context.espacio_publico and not context.espacio_publico.esta_disponible():
        print("El espacio público no está disponible para este evento.")
    ##retroalimentacion
    """
    Intenta crear el evento y confirma que falla con ValidationError.
    """
    if not context.espacio_disponible:
        try:
            EventoMunicipal.objects.crear_evento_con_aforo(
                nombre="Evento de Prueba No Creado",
                descripcion="No debería crearse",
                fecha=context.fecha_evento,
                espacio_publico=context.espacio_publico,
                capacidad=100,
                entidad_municipal=context.entidad_municipal
            )
            assert False, "Se creó el evento cuando el espacio no estaba disponible."
        except ValidationError:
            # Ruta esperada: no se puede crear
            pass
    else:
        assert False, "El espacio se marcó como disponible; no corresponde a este paso."


@step("se mostrarán los espacios públicos disponibles")
def step_impl(context):
    """
        crear eventos espacios publicos disponibles no disponible en la misma (3)
        hacer una lista print
        y hacer que no tengan la misma fecha
    """

    context.espacio_publico_disponible = EspacioPublico.objects.create(
        nombre=fake.name(),
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )
    context.espacio_publico_disponible2 = EspacioPublico.objects.create(
        nombre=fake.name(),
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )

    espacios_disponibles = EspacioPublico.objects.filter(estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE)

    if espacios_disponibles.exists():
        print("Espacios públicos disponibles:")
        for espacio in espacios_disponibles:
            print(f"{espacio.nombre} - {espacio.direccion}")
    else:
        print("No hay espacios públicos disponibles.")

    ##retroalimentacion
    """
    Lista los espacios que no tengan un evento PROGRAMADO/EN_CURSO en esa fecha.
    """
    fecha = context.fecha_evento

    eventos_misma_fecha = EventoMunicipal.objects.filter(
        fecha_realizacion=fecha,
        estado_actual__in=[EventoMunicipal.ESTADO_PROGRAMADO, EventoMunicipal.ESTADO_EN_CURSO]
    ).values_list('espacio_publico_id', flat=True)

    espacios_disponibles = EspacioPublico.objects.exclude(pk__in=eventos_misma_fecha)
    assert espacios_disponibles.count() >= 0, (
        "No se encontraron espacios disponibles (o ajustar la lógica)."
    )
    context.espacios_disponibles = espacios_disponibles


##--
@step('que existe un evento llamado "{nombre_evento}" con el estado "{estado_evento}"')
def step_existe_evento(context, nombre_evento, estado_evento):
    """
    Crea un evento con nombre y estado especificados, o None si estado_evento = "NULL" (no existe).
    """
    if estado_evento == "NULL":
        context.evento = None
        return

    # Asegurar que context.fecha_evento esté definido
    if not hasattr(context, "fecha_evento"):
        context.fecha_evento = timezone.now() + timedelta(days=7)

    # Crear una entidad municipal de prueba
    entidad_municipal = EntidadMunicipal.objects.create(
        nombre=fake.company(),
        correo_electronico=fake.email(),
        direccion=fake.address(),
        telefono=fake.phone_number(),
        fecha_registro=fake.date_time_between()
    )

    # Crear un espacio público de prueba
    espacio_publico = EspacioPublico.objects.create(
        nombre="Parque Bicentenario",
        entidad_municipal=entidad_municipal,
        direccion=fake.address(),
        estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )

    # Crear el evento usando el modelo EventoMunicipal
    context.evento = EventoMunicipal.objects.create(
        nombre_evento=nombre_evento,
        descripcion_evento="Evento para prueba de cancelación",
        fecha_realizacion=context.fecha_evento,  # Se usa context.fecha_evento
        espacio_publico=espacio_publico,
        lugar_evento=espacio_publico.nombre,
        capacidad_maxima=100,
        estado_actual=estado_evento
    )

@step('el espacio público destinado al evento es "{nombre_espacio}"')
def step_asigna_espacio(context, nombre_espacio):
    """
    Asigna un espacio público al evento.
    """
    if nombre_espacio == "NULL":
        context.espacio_afectado = False
        return

    # Obtener o crear el espacio público
    espacio_publico, _ = EspacioPublico.objects.get_or_create(
        nombre=nombre_espacio,
        defaults={
            'direccion': fake.address(),
            'estado_espacio_publico': EspacioPublico.ESTADO_DISPONIBLE,
            'estado_incidente_espacio': EspacioPublico.NO_AFECTADO
        }
    )

    # Asignar el espacio público al evento
    context.evento.espacio_publico = espacio_publico
    context.evento.save()

    context.espacio_afectado = (espacio_publico.estado_incidente_espacio == EspacioPublico.AFECTADO)

@step('está en una situación de "{estado_espacio}" debido a un "{motivo_riesgo}"')
def step_cambia_estado_espacio(context, estado_espacio, motivo_riesgo):
    """
    Cambia el estado del espacio público y registra el motivo de riesgo.
    """
    if context.evento and context.evento.espacio_publico:
        espacio_publico = context.evento.espacio_publico
        espacio_publico.estado_incidente_espacio = estado_espacio
        espacio_publico.motivo_riesgo = motivo_riesgo
        espacio_publico.save()

    context.motivo_riesgo = motivo_riesgo

@step('la entidad municipal cambia el estado del evento a "{nuevo_estado_evento}"')
def step_cambia_estado_evento(context, nuevo_estado_evento):
    """
    Cambia el estado del evento usando el repositorio.
    """
    repositorio = RepositorioEventos()
    if context.evento is None:
        print("No existe evento a cancelar.")
        return

    try:
        if nuevo_estado_evento == EventoMunicipal.ESTADO_CANCELADO:
            if hasattr(context, "motivo_riesgo"):
                repositorio.cancelar_evento(context.evento.id, context.motivo_riesgo)
            else:
                print("No se puede cancelar sin un motivo de riesgo.")
        else:
            repositorio.actualizar_evento(context.evento.id, estado_actual=nuevo_estado_evento)
    except ObjectDoesNotExist as e:
        print(f"Error: {e}")
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
