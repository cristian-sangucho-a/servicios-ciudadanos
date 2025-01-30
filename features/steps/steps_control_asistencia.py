"""
Steps para probar el control de asistencia a eventos municipales.
Implementa los pasos definidos en el archivo control_asistencia.feature
"""

from behave import given, when, then
from django.utils import timezone
from datetime import timedelta
from faker import Faker
from django.core import mail
from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal, ErrorGestionEventos
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia

fake = Faker('es_ES')  # Usamos el locale español

def crear_ciudadano_aleatorio():
    """Crea un ciudadano con datos aleatorios"""
    return Ciudadano.objects.create(
        correo_electronico=fake.email(),
        nombre_completo=f"{fake.first_name()} {fake.last_name()}",
        numero_identificacion=str(fake.random_number(digits=10, fix_len=True))
    )

def crear_evento_aleatorio(capacidad=10):
    """Crea un evento con datos aleatorios y capacidad específica"""
    return EventoMunicipal.objects.crear_evento_con_aforo(
        nombre=fake.sentence(nb_words=4),
        descripcion=fake.text(max_nb_chars=200),
        fecha=timezone.now() + timedelta(days=7),
        lugar=fake.address(),
        capacidad=capacidad
    )

# Escenario: Registro exitoso dentro del límite de aforo
@given("que existe un evento con aforo disponible")
def step_crear_evento_disponible(context):
    """Crea un evento programado con cupos disponibles"""
    context.evento = crear_evento_aleatorio()

@given("el ciudadano cumple con los requisitos de inscripción")
def step_crear_ciudadano(context):
    """Crea un ciudadano que cumple con los requisitos"""
    context.ciudadano = crear_ciudadano_aleatorio()

@when("el ciudadano intenta registrarse en el evento")
def step_inscribir_ciudadano(context):
    """Intenta registrar al ciudadano en el evento"""
    try:
        context.registro = context.evento.inscribir_ciudadano(context.ciudadano)
        context.error = None
    except ErrorGestionEventos as e:
        context.error = str(e)

@then("el sistema debe permitir el registro")
def step_verificar_registro_exitoso(context):
    """Verifica que el registro fue exitoso"""
    assert context.error is None, f"Error al registrar: {context.error}"
    assert context.registro.estado_registro == RegistroAsistencia.ESTADO_INSCRITO, "Estado de registro incorrecto"

@then("enviar una confirmación de inscripción por correo electrónico")
def step_verificar_correo_confirmacion(context):
    """Verifica que se envió el correo de confirmación"""
    # TODO: Implementar cuando se desarrolle la funcionalidad de correos
    pass

@then("reducir un cupo disponible del evento")
def step_verificar_reduccion_cupo(context):
    """Verifica que se redujo el cupo del evento"""
    evento_actualizado = EventoMunicipal.objects.get(pk=context.evento.pk)
    assert evento_actualizado.cupos_disponibles == context.evento.capacidad_maxima - 1, "Cupo no reducido"

# Escenario: Intento de registro cuando el evento está lleno
@given("que existe un evento con aforo lleno")
def step_crear_evento_lleno(context):
    """Crea un evento sin cupos disponibles"""
    context.evento = crear_evento_aleatorio(capacidad=1)
    ciudadano_inicial = crear_ciudadano_aleatorio()
    context.evento.inscribir_ciudadano(ciudadano_inicial)

@when("un ciudadano intenta registrarse en el evento")
def step_inscribir_ciudadano_evento_lleno(context):
    """Intenta registrar a un nuevo ciudadano en el evento lleno"""
    context.ciudadano = crear_ciudadano_aleatorio()
    try:
        context.registro = context.evento.inscribir_ciudadano(context.ciudadano)
        context.error = None
    except ErrorGestionEventos as e:
        context.error = str(e)
        context.registro = None

@then("el sistema debe rechazar el registro directo")
def step_verificar_registro_rechazado(context):
    """Verifica que el registro fue rechazado y agregado a la lista de espera"""
    assert context.error is None, f"Error inesperado: {context.error}"
    assert context.registro is not None, "No se creó el registro"
    assert context.registro.estado_registro == RegistroAsistencia.ESTADO_EN_ESPERA, "Estado incorrecto"

@then("agregar al ciudadano a una lista de espera")
def step_verificar_lista_espera(context):
    """Verifica que el ciudadano está en lista de espera"""
    lista_espera = list(context.evento.obtener_lista_espera())
    assert context.registro in lista_espera, "Registro no encontrado en lista de espera"

@then("notificar al ciudadano de su estado en la lista de espera")
def step_verificar_notificacion_lista_espera(context):
    """Verifica que se notificó al ciudadano sobre la lista de espera"""
    # TODO: Implementar cuando se desarrolle la funcionalidad de correos
    pass

# Escenario: Cancelación de inscripción por parte del ciudadano
@given("que un ciudadano está inscrito en un evento")
def step_crear_evento_con_inscripcion(context):
    """Crea un evento y registra un ciudadano"""
    context.evento = crear_evento_aleatorio(capacidad=2)
    context.ciudadano = crear_ciudadano_aleatorio()
    context.registro = context.evento.inscribir_ciudadano(context.ciudadano)

@given("hay otro ciudadano en lista de espera")
def step_agregar_ciudadano_espera(context):
    """Agrega un ciudadano a la lista de espera"""
    context.ciudadano_espera = crear_ciudadano_aleatorio()
    context.registro_espera = context.evento.inscribir_ciudadano(context.ciudadano_espera)

@when("el ciudadano decide cancelar su inscripción")
def step_cancelar_inscripcion(context):
    """Cancela la inscripción del ciudadano"""
    try:
        context.registro_cancelado, context.registro_promovido = context.evento.cancelar_inscripcion(context.registro.id)
        context.error = None
    except ErrorGestionEventos as e:
        context.error = str(e)
        context.registro_cancelado = context.registro_promovido = None

@then("el sistema debe liberar el cupo correspondiente")
def step_verificar_liberacion_cupo(context):
    """Verifica que se liberó el cupo y se canceló el registro"""
    assert context.error is None, f"Error al cancelar: {context.error}"
    assert context.registro_cancelado is not None, "No se canceló el registro"
    assert context.registro_cancelado.estado_registro == RegistroAsistencia.ESTADO_CANCELADO, "Estado incorrecto"

@then("el primer ciudadano en lista de espera debe ser registrado automáticamente")
def step_verificar_promocion_espera(context):
    """Verifica que se promovió al ciudadano en espera"""
    registro_actualizado = RegistroAsistencia.objects.get(pk=context.registro_espera.pk)
    assert registro_actualizado.estado_registro == RegistroAsistencia.ESTADO_INSCRITO, "No se promovió el registro"

@then("notificar al ciudadano promovido de la lista de espera")
def step_verificar_notificacion_promocion(context):
    """Verifica que se notificó al ciudadano promovido"""
    # TODO: Implementar cuando se desarrolle la funcionalidad de correos
    pass
