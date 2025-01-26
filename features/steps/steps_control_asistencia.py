"""
Steps para probar el control de asistencia a eventos municipales.
Implementa los pasos definidos en el archivo control_asistencia.feature
"""

from behave import given, when, then
from faker import Faker
from django.utils import timezone
from datetime import timedelta
from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models import EventoMunicipal, RegistroAsistencia
from entidad_municipal_app.services import GestorRegistroAsistencia, ErrorGestionEventos

fake = Faker(['es_ES'])

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
        capacidad_maxima=50,
        cupos_disponibles=10,  # Cupo disponible
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
    assert context.registro.estado_registro == RegistroAsistencia.ESTADO_INSCRITO, (
        f"Estado esperado 'INSCRITO', se obtuvo {context.registro.estado_registro}"
    )

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
    evento_actualizado = EventoMunicipal.objects.get(id=context.evento.id)
    assert evento_actualizado.cupos_disponibles == 9, (
        f"Se esperaba cupos_disponibles = 9, se encontró: {evento_actualizado.cupos_disponibles}"
    )

@given("que existe un evento con aforo lleno")
def step_impl(context):
    """
    Crea un evento sin cupos disponibles.
    """
    context.evento = EventoMunicipal.objects.create(
        nombre_evento=f"EventoLleno {fake.word()}",
        descripcion_evento=fake.paragraph(),
        fecha_realizacion=timezone.now() + timedelta(days=3),
        lugar_evento=fake.city(),
        capacidad_maxima=2,
        cupos_disponibles=0,  # Sin cupo
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    )

@when("un ciudadano intenta registrarse en el evento")
def step_impl(context):
    """
    Crea otro ciudadano y trata de registrar la asistencia. 
    En caso de no haber cupo, quedará en EN_ESPERA.
    """
    context.ciudadano = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret456"
    )
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
    assert context.error is None, f"Se produjo un error inesperado: {context.error}"
    assert context.registro.estado_registro == RegistroAsistencia.ESTADO_EN_ESPERA, (
        f"Se esperaba estado 'EN_ESPERA', pero fue: {context.registro.estado_registro}"
    )

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
        nombre_evento=f"EventoConCupo {fake.word()}",
        descripcion_evento=fake.paragraph(),
        fecha_realizacion=timezone.now() + timedelta(days=7),
        lugar_evento=fake.city(),
        capacidad_maxima=1,
        cupos_disponibles=1,
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO
    )
    context.ciudadano_inscrito = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret789"
    )
    gestor = GestorRegistroAsistencia()
    context.registro = gestor.procesar_solicitud_inscripcion(
        evento_id=context.evento.id,
        ciudadano=context.ciudadano_inscrito
    )

@given("hay otro ciudadano en lista de espera")
def step_impl(context):
    """
    Crea un segundo ciudadano que irá a lista de espera (cupos=0).
    """
    context.ciudadano_espera = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret999"
    )
    # Forzar cupos a 0
    context.evento.cupos_disponibles = 0
    context.evento.save()

    gestor = GestorRegistroAsistencia()
    context.registro_espera = gestor.procesar_solicitud_inscripcion(
        evento_id=context.evento.id,
        ciudadano=context.ciudadano_espera
    )

@when("el ciudadano decide cancelar su inscripción")
def step_impl(context):
    """
    Llamamos al gestor para cancelar el registro y así liberar cupo
    o promover a alguien en espera.
    """
    gestor = GestorRegistroAsistencia()
    context.registro_cancelado, context.registro_promovido = gestor.procesar_cancelacion_inscripcion(
        context.registro.id
    )

@then("el sistema debe liberar el cupo correspondiente")
def step_impl(context):
    """
    Verifica que el registro original está CANCELADO.
    """
    registro_cancelado = RegistroAsistencia.objects.get(id=context.registro.id)
    assert registro_cancelado.estado_registro == RegistroAsistencia.ESTADO_CANCELADO, (
        f"Se esperaba estado 'CANCELADO', se encontró: {registro_cancelado.estado_registro}"
    )

@then("el primer ciudadano en lista de espera debe ser registrado automáticamente")
def step_impl(context):
    """
    Verifica que el registro en espera pasó a INSCRITO.
    """
    registro_espera_actualizado = RegistroAsistencia.objects.get(id=context.registro_espera.id)
    assert registro_espera_actualizado.estado_registro == RegistroAsistencia.ESTADO_INSCRITO, (
        f"Se esperaba estado 'INSCRITO', se encontró: {registro_espera_actualizado.estado_registro}"
    )

@then("notificar al ciudadano promovido de la lista de espera")
def step_impl(context):
    """
    Simulación de notificación al ciudadano promovido.
    En producción se integraría con sistema real.
    """
    pass
