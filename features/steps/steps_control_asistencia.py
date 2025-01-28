"""
Steps para probar el control de asistencia a eventos municipales.
Implementa los pasos definidos en el archivo control_asistencia.feature
"""

from behave import given, when, then
from django.utils import timezone
from datetime import timedelta
from faker import Faker
from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.registro_asistencia import RegistroAsistencia
from entidad_municipal_app.services import GestorRegistroAsistencia, ErrorGestionEventos

fake = Faker()

@given("que existe un evento con aforo disponible")
def step_impl(context):
    """
    Crea un evento programado con cupos disponibles.
    Guarda el evento en context.evento para pasos posteriores.
    """
    context.evento = EventoMunicipal.objects.create(
        nombre_evento=f"Evento {fake.word()}",
        descripcion_evento=fake.paragraph(),
        fecha_realizacion=timezone.now() + timedelta(days=5),
        lugar_evento=fake.city(),
        capacidad_maxima=10,
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    )

@given("el ciudadano cumple con los requisitos de inscripción")
def step_impl(context):
    """
    Crea un ciudadano ficticio usando Faker. Guarda la instancia en context.ciudadano.
    """
    context.ciudadano = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    )

@when("el ciudadano intenta registrarse en el evento")
def step_impl(context):
    """
    Llama al gestor para registrar la asistencia.
    Si ocurre un error, se guarda en context.error.
    """
    try:
        gestor = GestorRegistroAsistencia()
        context.registro = gestor.procesar_solicitud_inscripcion(
            evento_id=context.evento.id,
            ciudadano=context.ciudadano
        )
        context.error = None
    except ErrorGestionEventos as e:
        context.error = str(e)

@then("el sistema debe permitir el registro")
def step_impl(context):
    """
    Verifica que no haya error y que el registro esté en estado INSCRITO.
    """
    assert context.error is None, f"Se esperaba que no hubiera error, pero ocurrió: {context.error}"
    assert context.registro.estado_registro == RegistroAsistencia.ESTADO_INSCRITO

@then("enviar una confirmación de inscripción por correo electrónico")
def step_impl(context):
    """
    En esta demo, simulamos el envío de email. En producción se integraría con sistema real.
    """
    pass

@then("reducir un cupo disponible del evento")
def step_impl(context):
    """
    Confirma que los cupos disponibles del evento se redujeron en 1.
    """
    evento = EventoMunicipal.objects.get(pk=context.evento.id)
    assert evento.cupos_disponibles == context.evento.capacidad_maxima - 1

@given("que existe un evento con aforo lleno")
def step_impl(context):
    """
    Crea un evento sin cupos disponibles.
    """
    context.evento = EventoMunicipal.objects.create(
        nombre_evento=f"Evento {fake.word()}",
        descripcion_evento=fake.paragraph(),
        fecha_realizacion=timezone.now() + timedelta(days=5),
        lugar_evento=fake.city(),
        capacidad_maxima=1,  # Solo un cupo
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    )
    
    # Crear y registrar un ciudadano para llenar el cupo
    ciudadano = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    )
    
    # Registrar al ciudadano usando el gestor
    gestor = GestorRegistroAsistencia()
    gestor.procesar_solicitud_inscripcion(
        evento_id=context.evento.id,
        ciudadano=ciudadano
    )

@when("un ciudadano intenta registrarse en el evento")
def step_impl(context):
    """
    Crea otro ciudadano y trata de registrar la asistencia. 
    En caso de no haber cupo, quedará en EN_ESPERA.
    """
    # Crear otro ciudadano
    context.ciudadano = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    )
    
    # Intentar registrarlo
    try:
        gestor = GestorRegistroAsistencia()
        context.registro = gestor.procesar_solicitud_inscripcion(
            evento_id=context.evento.id,
            ciudadano=context.ciudadano
        )
        context.error = None
    except ErrorGestionEventos as e:
        context.error = str(e)

@then("el sistema debe rechazar el registro directo")
def step_impl(context):
    """
    Verifica que el registro quedó en estado EN_ESPERA.
    """
    assert context.registro.estado_registro == RegistroAsistencia.ESTADO_EN_ESPERA

@then("agregar al ciudadano a una lista de espera")
def step_impl(context):
    """
    Confirma que el registro está en EN_ESPERA.
    """
    assert context.registro.estado_registro == RegistroAsistencia.ESTADO_EN_ESPERA

@then("notificar al ciudadano de su estado en la lista de espera")
def step_impl(context):
    """
    Simulación de notificación. En producción se integraría con sistema real.
    """
    pass

@given("que un ciudadano está inscrito en un evento")
def step_impl(context):
    """
    Creamos un evento con cupo y un ciudadano inscrito directamente.
    """
    context.evento = EventoMunicipal.objects.create(
        nombre_evento=f"Evento {fake.word()}",
        descripcion_evento=fake.paragraph(),
        fecha_realizacion=timezone.now() + timedelta(days=5),
        lugar_evento=fake.city(),
        capacidad_maxima=1,  # Solo un cupo
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    )
    
    # Crear y guardar el primer ciudadano
    context.ciudadano = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    )
    
    # Crear el registro usando el gestor
    gestor = GestorRegistroAsistencia()
    context.registro = gestor.procesar_solicitud_inscripcion(
        evento_id=context.evento.id,
        ciudadano=context.ciudadano
    )

@given("hay otro ciudadano en lista de espera")
def step_impl(context):
    """
    Crea un segundo ciudadano que irá a lista de espera.
    """
    # Crear el segundo ciudadano
    context.ciudadano_espera = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    )
    
    # Intentar registrarlo (quedará en espera porque no hay cupos)
    gestor = GestorRegistroAsistencia()
    context.registro_espera = gestor.procesar_solicitud_inscripcion(
        evento_id=context.evento.id,
        ciudadano=context.ciudadano_espera
    )
    
    # Verificar que quedó en lista de espera
    assert context.registro_espera.estado_registro == RegistroAsistencia.ESTADO_EN_ESPERA, (
        f"Se esperaba estado EN_ESPERA, se encontró: {context.registro_espera.estado_registro}"
    )

@when("el ciudadano decide cancelar su inscripción")
def step_impl(context):
    """
    Llamamos al gestor para cancelar el registro y así liberar cupo
    o promover a alguien en espera.
    """
    gestor = GestorRegistroAsistencia()
    context.registro_cancelado, context.registro_promovido = gestor.procesar_cancelacion_inscripcion(
        registro_id=context.registro.id
    )

@then("el sistema debe liberar el cupo correspondiente")
def step_impl(context):
    """
    Verifica que el registro original está CANCELADO.
    """
    assert context.registro_cancelado.estado_registro == RegistroAsistencia.ESTADO_CANCELADO

@then("el primer ciudadano en lista de espera debe ser registrado automáticamente")
def step_impl(context):
    """
    Verifica que el registro en espera pasó a INSCRITO.
    """
    assert context.registro_promovido.estado_registro == RegistroAsistencia.ESTADO_INSCRITO

@then("notificar al ciudadano promovido de la lista de espera")
def step_impl(context):
    """
    Simulación de notificación al ciudadano promovido.
    En producción se integraría con sistema real.
    """
    pass
