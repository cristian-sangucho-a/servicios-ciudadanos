from behave import given, when, then
from faker import Faker
from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo, Suscripcion
from entidad_municipal_app.models.canales.noticia import Noticia
import string
import secrets

from entidad_municipal_app.models.canales.sugerencia import Sugerencia
from shared.models.notificacion.notificacion import Notificacion

fake = Faker()

def generate_random_string(length):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# --- Métodos Auxiliares ---
def crear_ciudadano():
    """Crea y retorna un ciudadano ficticio."""
    return Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        password=generate_random_string(7)
    )

def crear_canal(nombre, es_emergencia=False):
    """Crea una entidad para asociarla al canal"""
    entidad = EntidadMunicipal.objects.create_user(
        correo_electronico= fake.email(),
        password=generate_random_string(7)
    )
    """Crea y retorna un canal informativo o de emergencia."""
    canal = CanalInformativo.crear_canal(entidad,nombre,"Canal de noticias",es_emergencia)
    return canal

# --- Escenario de suscripción a un canal informativo ---
@given('que soy una entidad municipal que gestiona el canal "{canal_nombre}",')
def step_impl(context, canal_nombre):
    """Crea un canal informativo."""
    context.canal = crear_canal(canal_nombre, es_emergencia=False)


@when('el ciudadano activa su suscripción al canal "{canal_nombre}",')
def step_impl(context, canal_nombre):
    """El ciudadano se suscribe al canal especificado."""
    context.ciudadano = crear_ciudadano()
    context.suscripcion = context.canal.suscribir_ciudadano(context.ciudadano)

    assert context.suscripcion, f"El ciudadano no se suscribió correctamente al canal {canal_nombre}."


@then("el ciudadano recibe noticias relacionadas al canal.")
def step_impl(context):
    """Verifica que el ciudadano recibe noticias del canal suscrito."""
    Noticia.crear_noticia(context.canal,fake.sentence(),fake.text(max_nb_chars=500) )
    noticias = context.canal.noticias
    assert noticias.exists(), f"No hay noticias en el canal {context.canal.nombre}."


# --- Escenario de reacción y comentario en una noticia ---
@given("existe un ciudadano registrado")
def step_impl(context):
    """Crea un ciudadano ficticio."""
    context.ciudadano = crear_ciudadano()


@given("existe una noticia publicada en un canal informativo")
def step_impl(context):
    """Crea un canal informativo y publica una noticia."""
    context.canal = crear_canal("Noticias Locales")
    context.noticia = Noticia.crear_noticia(context.canal,
        fake.sentence(),
        fake.text(max_nb_chars=500))


@when('el ciudadano reacciona a la noticia con "{tipo_reaccion}"')
def step_impl(context, tipo_reaccion):
    """Registra la reacción del ciudadano en la noticia."""
    context.noticia.reaccionar(context.ciudadano,tipo_reaccion)


@when('el ciudadano comenta en la noticia con "{comentario_texto}"')
def step_impl(context, comentario_texto):
    """Registra un comentario en la noticia."""
    context.noticia.comentar(context.ciudadano,comentario_texto)


@then("la reacción y comentario del ciudadano quedan registrados en la noticia.")
def step_impl(context):
    """Verifica que la reacción y comentario han sido almacenados."""
    assert context.noticia.obtener_reacciones().exists(), "La reacción no fue registrada."
    assert context.noticia.obtener_comentarios().exists(), "El comentario no fue registrado."


# --- Escenario de alertas de emergencia ---
@given('que soy una entidad municipal que gestiona el canal de "{canal_nombre}",')
def step_impl(context, canal_nombre):
    """Crea un canal de emergencia y suscribe ciudadanos ficticios."""
    numero_de_ciudadanos = 5
    context.canal_emergencia = crear_canal(canal_nombre, es_emergencia=True)
    context.ciudadanos_en_ciudad = [crear_ciudadano() for _ in range(numero_de_ciudadanos)]
    suscripciones = []

    for ciudadano in context.ciudadanos_en_ciudad:
        suscripciones.append(context.canal_emergencia.suscribir_ciudadano(ciudadano))

    assert len(suscripciones) == numero_de_ciudadanos, "Los ciudadanos no fueron suscritos correctamente al canal de emergencia."


@when('ocurre un incidente "{incidente}" en "{ciudad}",')
def step_impl(context, incidente, ciudad):
    """Guarda la información del incidente."""
    context.incidente = incidente
    context.ciudad = ciudad


@then('el sistema envía alertas rápidas a los ciudadanos de "{ciudad}".')
def step_impl(context, ciudad):
    """Verifica que las alertas de emergencia han sido enviadas."""
    context.canal_emergencia.notificar_alerta_emergencia(context.incidente, context.ciudad)
    assert Notificacion.objects.filter(titulo = "Alerta de emergencia").exists(), 'No se han eviado alertas de emergencia'


@given("que soy un ciudadano registrado")
def step_impl(context):
    """Crea un ciudadano ficticio."""
    context.ciudadano = crear_ciudadano()

@when('el ciudadano crea una sugerencia de canal con nombre "{nombre}" y descripción "{descripcion}"')
def step_impl(context, nombre, descripcion):
    Sugerencia.crear_sugerencia_canal(nombre, descripcion)

@then("el sistema registra la sugerencia del ciudadano")
def step_impl(context):
    """Verifica que la sugerencia ha sido almacenada."""
    assert Sugerencia.obtener_sugerencias().exists(), "La sugerencia no fue registrada."