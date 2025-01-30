from behave import *
import random
from faker import Faker
from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.espacio_publico import EspacioPublico
from entidad_municipal_app.models import EventoMunicipal

#use_step_matcher("re")
ecuador_cities = [
    "Quito", "Guayaquil", "Cuenca", "Ambato", "Loja", "Manta", "Riobamba", "Durán",
    "Machala", "Esmeraldas", "Santo Domingo", "Ibarra", "Portoviejo", "Tena", "Babahoyo",
    "Quevedo", "Latacunga", "Salinas", "Tulcán", "Chone", "Puyo", "Cayambe"
]

fake = Faker()

@step("que una entidad municipal desea organizar un evento")
def step_impl(context):
    ciudad = random.choice(ecuador_cities)
    context.nombre_entidad_municipal = f"Municipio de {ciudad}"
    context.entidad_municipal = EntidadMunicipal.objects.create(
        nombre=context.nombre_entidad_municipal,
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email()
    )
    context.nombre_evento = f"Evento {fake.word()}"

@step('la fecha del evento es {fecha_evento}')
def step_impl(context,fecha_evento):
    context.fecha_realizacion = fake.date_time().strftime("%Y-%m-%d %H:%M:%S")


@step('el espacio público {nombre_espacioPublico} que se encuentra disponible')
def step_impl(context, nombre_espacioPublico):
    """
    Verifica que el espacio público con el nombre dado está disponible.
    Si está disponible, lo guarda en context.espacio_publico.
    Si no está disponible, imprime un mensaje.

    :param context: Contexto de Behave.
    :param nombre_espacioPublico: Nombre del espacio público a verificar.
    """
    # Obtener el espacio público por nombre
    espacio_publico = EspacioPublico.obtener_por_nombre(nombre_espacioPublico)

    # Verificar si el espacio público existe
    if espacio_publico is None:
        print(f"No se encontró el espacio público: {nombre_espacioPublico}")
        context.espacio_publico = None  # Guardar None en el contexto
        return

    # Verificar si el espacio público está disponible
    if espacio_publico.estado_espacioPublico == EspacioPublico.ESTADO_DISPONIBLE:
        print(f"El espacio público '{nombre_espacioPublico}' está disponible.")
        context.espacio_publico = espacio_publico  # Guardar en el contexto
    else:
        print(f"El espacio público '{nombre_espacioPublico}' no está disponible. Estado actual: {espacio_publico.estado_espacioPublico}")
        context.espacio_publico = None  # Guardar None en el contexto


@step("se creara el evento")
def step_impl(context):
    # Verificar disponibilidad
    print("El espacio público no está disponible para este evento.")
    #if context.espacio_publico.esta_disponible():
    context.evento = EventoMunicipal.objects.create(
        nombre_evento=context.nombre_evento,
        descripcion_evento=fake.paragraph(),
        fecha_realizacion=context.fecha_realizacion,
        lugar_evento=context.espacio_publico,  # Asegúrate de usar la instancia de EspacioPublico
        capacidad_maxima=10,
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    )
    #print(context.evento)
    print("Evento creado con los siguientes detalles:")
    print(f"Nombre: {context.evento.nombre_evento}")
    print(f"Descripción: {context.evento.descripcion_evento}")
    print(f"Fecha: {context.evento.fecha_realizacion}")
    print(f"Lugar: {context.evento.lugar_evento}")
    print(f"Capacidad: {context.evento.capacidad_maxima}")
    print(f"Estado: {context.evento.estado_actual}")

@step('el espacio público "{nombre_espacioPublico}" no se encuentre disponible')
def step_impl(context, nombre_espacioPublico):
    """
       Verifica que el espacio público con el nombre dado está disponible.
       Si está disponible, lo guarda en context.espacio_publico.
       Si no está disponible, imprime un mensaje.

       :param context: Contexto de Behave.
       :param nombre_espacioPublico: Nombre del espacio público a verificar.
       """
    # Obtener el espacio público por nombre
    espacio_publico = EspacioPublico.obtener_por_nombre(nombre_espacioPublico)

    # Verificar si el espacio público existe
    if espacio_publico is None:
        print(f"No se encontró el espacio público: {nombre_espacioPublico}")
        context.espacio_publico = None  # Guardar None en el contexto
        return

    # Verificar si el espacio público está disponible
    if espacio_publico.estado_espacioPublico == EspacioPublico.ESTADO_DISPONIBLE:
        print(f"El espacio público '{nombre_espacioPublico}' está disponible.")
        context.espacio_publico = espacio_publico  # Guardar en el contexto
    else:
        print(
            f"El espacio público '{nombre_espacioPublico}' no está disponible. Estado actual: {espacio_publico.estado_espacioPublico}")
        context.espacio_publico = None  # Guardar None en el contexto



@step("no se creara el evento")
def step_impl(context):
    context.espacio_publico = None

@step("se mostrarán los espacios públicos disponibles")
def step_impl(context):
    espacios_disponibles = EspacioPublico.objects.filter(estado_espacioPublico=EspacioPublico.ESTADO_DISPONIBLE)

    if espacios_disponibles.exists():
        print("Espacios públicos disponibles:")
        for espacio in espacios_disponibles:
            print(f"{espacio.nombre} - {espacio.direccion}")
    else:
        print("No hay espacios públicos disponibles.")


##--
@step('que existe un evento llamado "{nombre_evento}" con el estado "{estado_evento}"')
def step_impl(context, nombre_evento, estado_evento):
    AssertionError("Not implemented")


@step(
    'el espacio público destinado al evento "{nombre_espacio}" está en una situación de "{estado_espacio}" debido a un "{motivoRiesgo}"')
def step_impl(context, nombre_espacio, estado_espacio, motivoRiesgo):
    AssertionError("Not implemented")

@step('la entidad municipal cambia el estado del evento a "{nuevo_estado_evento}"')
def step_impl(context, nuevo_estado_evento):
    AssertionError("Not implemented")


@step('se registra el motivo de la cancelación "{resultado}"')
def step_impl(context, resultado):
    AssertionError("Not implemented")
