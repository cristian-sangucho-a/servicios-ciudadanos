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

@step('que la entidad municipal "Municipio de Quito" desea organizar el evento "Quito Fest"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Dado que la entidad municipal "Municipio de Quito" desea organizar el evento "Quito Fest"')


@step('la fecha del evento es "2023-12-06" con hora de inicio a las "14:00"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Y la fecha del evento es "2023-12-06" con hora de inicio a las "14:00"')


@step('el espacio público "Parque Central" se encuentre disponible')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando el espacio público "Parque Central" se encuentre disponible')


@step("se publicará el evento en la Agenda Pública")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces se publicará el evento en la Agenda Pública')


@step('el espacio público "Parque Central" no se encuentre disponible')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando el espacio público "Parque Central" no se encuentre disponible')


@step("no se incluirá el evento en la Agenda Pública")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces no se incluirá el evento en la Agenda Pública')


@step("se mostrarán los espacios públicos disponibles")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Y se mostrarán los espacios públicos disponibles')


@step("se registran mas de un espacio público para el evento")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando se registran los siguientes espacios públicos para el evento: ')


@step("todos los espacios públicos son distintos entre sí")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Y todos los espacios públicos son distintos entre sí')


@step("se incluirá el evento en la Agenda Pública")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces se incluirá el evento en la Agenda Pública')


@step('que existe un evento llamado "Festival Cultural de Primavera" con el estado "Confirmado"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Dado que existe un evento llamado "Festival Cultural de Primavera" con el estado "Confirmado"')


@step('el espacio público destinado al evento está en una situación de "Riesgo" debido a un "Incendio forestal"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(
        u'STEP: Y el espacio público destinado al evento está en una situación de "Riesgo" debido a un "Incendio forestal"')


@step('la entidad municipal cambia el estado del evento a "Cancelado"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Cuando la entidad municipal cambia el estado del evento a "Cancelado"')


@step("se registra el motivo de la cancelación")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    raise NotImplementedError(u'STEP: Entonces se registra el motivo de la cancelación')


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


@step('la fecha deseada del evento es 06/02/2025 14:00')
def step_impl(context):
    context.fecha_realizacion = fake.date_time().strftime("%Y-%m-%d %H:%M:%S")


@step('se añada el espacio público {nombre_espacioPublico} que se encuentra disponible')
def step_impl(context,nombre_espacioPublico):
    context.espacio_publico = EspacioPublico.objects.create(
        nombre=nombre_espacioPublico,
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        disponibilidad=True  # Marca como disponible
    )


@step("se agregara el evento en la Agenda Pública")
def step_impl(context):
    # Asegurarte de que el nombre o ID corresponda a un EspacioPublico

    # Verificar disponibilidad
    print("El espacio público no está disponible para este evento.")
    if context.espacio_publico.esta_disponible():
        context.evento = EventoMunicipal.objects.create(
            nombre_evento=context.nombre_evento,
            descripcion_evento=fake.paragraph(),
            fecha_realizacion=context.fecha_realizacion,
            lugar_evento=context.espacio_publico,  # Asegúrate de usar la instancia de EspacioPublico
            capacidad_maxima=10,
            estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
        )
