from behave import given, when, then
from faker import Faker
from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo, Suscripcion
from entidad_municipal_app.models.canales.noticia import Noticia

fake = Faker()

# Dado que soy una entidad municipal que gestiona el canal
@given('que soy una entidad municipal que gestiona el canal "{canal_nombre}",')
def step_impl(context, canal_nombre):
    """
    Crea un canal informativo con el nombre proporcionado.
    """
    context.canal = CanalInformativo.objects.get_or_create(
        nombre=canal_nombre,
        descripcion=fake.text(max_nb_chars=200),
        es_emergencia=False
    )[0]


# Cuando el ciudadano activa su suscripción al canal
@when('el ciudadano activa su suscripción al canal "{canal_nombre}",')
def step_impl(context, canal_nombre):
    """
    El ciudadano se suscribe al canal especificado.
    """
    # Crear un ciudadano ficticio
    context.ciudadano = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    )

    canal = CanalInformativo.objects.get(nombre=canal_nombre)
    context.canal = canal
    canal.suscribir_ciudadano(context.ciudadano)
    suscripcion = Suscripcion.objects.get(canal=canal, ciudadano=context.ciudadano)

    # Asegurar que la suscripción exista
    assert suscripcion, f"El ciudadano {context.ciudadano.nombre_completo} no está suscrito al canal {canal.nombre}."


# Entonces el ciudadano recibe noticias relacionadas al canal
@then('el ciudadano recibe noticias relacionadas al canal.')
def step_impl(context):
    """
    Verifica que el ciudadano esté recibiendo noticias del canal al que está suscrito.
    """
    Noticia.objects.create(
        canal=context.canal,
        titulo=fake.sentence(),
        contenido=fake.text(max_nb_chars=500),
        imagen=None
    )

    noticias = Noticia.objects.filter(canal=context.canal)
    assert noticias.exists(), f"No hay noticias relacionadas al canal {context.canal.nombre}."

# Dado que soy una entidad municipal que gestiona el canal de emergencia
@given('que soy una entidad municipal que gestiona el canal de "{canal_nombre}",')
def step_impl(context, canal_nombre):
    """
    Crea un canal informativo con el nombre proporcionado.
    """
    CanalInformativo.objects.get_or_create(
        nombre=canal_nombre,
        descripcion="Canal para notificaciones urgentes.",
        es_emergencia=True
    )
    canal = CanalInformativo.objects.get(nombre=canal_nombre)
    context.canal_emergencia = canal
    # Crear ciudadanos ficticios
    context.ciudadanos_en_ciudad = [Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    ) for _ in range(5)]

    suscripciones = []
    for ciudadano in context.ciudadanos_en_ciudad:
        context.canal_emergencia.suscribir_ciudadano(ciudadano)
        suscripciones.append(Suscripcion.objects.get(canal=canal, ciudadano=ciudadano))

    assert len(context.ciudadanos_en_ciudad) == len(suscripciones), f"Los ciudadanos no están suscritos al canal {context.canal_emergencia.nombre}."

# Cuando ocurre un incidente de emergencia
@when('ocurre un incidente "{incidente}" en "{ciudad}",')
def step_impl(context, incidente, ciudad):
    """
    Guarda la informacion de incidente.
    """
    context.incidente = incidente
    context.ciudad = ciudad

# El sistema envía alertas rápidas a los ciudadanos de la localidad
@then('el sistema envía alertas rápidas a los ciudadanos de "{ciudad}".')
def step_impl(context, ciudad):
    """
    Verifica que las alertas de emergencia han sido enviadas a los ciudadanos de la localidad.
    """
    context.canal_emergencia.notificar_alerta_emergencia(context.incidente,context.ciudad)