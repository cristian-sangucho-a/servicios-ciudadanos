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
    #print("El espacio público no está disponible para este evento.")
    if context.espacio_publico.esta_disponible():
        context.evento = EventoMunicipal.objects.create(
            nombre_evento=context.nombre_evento,
            descripcion_evento=fake.paragraph(),
            fecha_realizacion=context.fecha_realizacion,
            lugar_evento=context.espacio_publico,  # Asegúrate de usar la instancia de EspacioPublico
            capacidad_maxima=10,
            estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
        )
    else:
        print("El espacio público no está disponible para este evento.")
