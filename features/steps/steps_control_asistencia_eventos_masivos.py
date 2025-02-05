"""
Steps para probar el control de asistencia a eventos municipales.
Implementa los pasos definidos en el archivo control_asistencia.feature
"""

from behave import given, when, then
from django.utils import timezone
from datetime import timedelta
from datetime import datetime
from django.core import mail
from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal, ErrorGestionEventos  
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from mocks.repositorio_eventos_memoria import (
    crear_ciudadano_aleatorio,
    crear_entidad_municipal_aleatoria,
    crear_espacio_publico_aleatorio,
    crear_evento_aleatorio
)

# Escenario: Registro exitoso dentro del límite de aforo
@given("que existe un evento con aforo disponible")
def step_crear_evento_disponible(context):
    """Crea un evento programado con cupos disponibles"""
    # Limpiar el buzón de correo antes de cada escenario
    mail.outbox = []
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
    # Verificar que hay al menos un correo en la bandeja de salida
    assert len(mail.outbox) > 0, "No se envió ningún correo"
    
    # Buscar el correo enviado al ciudadano
    correo_encontrado = False
    for email in mail.outbox:
        if context.ciudadano.correo_electronico in email.to:
            correo_encontrado = True
            # Verificar que es un correo de confirmación de inscripción
            assert "confirmación" in email.subject.lower(), "El asunto no indica que es una confirmación"
            assert context.evento.nombre_evento in email.subject, "El asunto no contiene el nombre del evento"
            break
    
    assert correo_encontrado, "No se encontró el correo de confirmación para el ciudadano"

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
    # Verificar que hay al menos un correo en la bandeja de salida
    assert len(mail.outbox) > 0, "No se envió ningún correo"
    
    # Buscar el correo enviado al ciudadano
    correo_encontrado = False
    for email in mail.outbox:
        if context.ciudadano.correo_electronico in email.to:
            correo_encontrado = True
            # Verificar que es un correo de lista de espera
            assert "lista de espera" in email.subject.lower(), "El asunto no indica lista de espera"
            assert context.evento.nombre_evento in email.subject, "El asunto no contiene el nombre del evento"
            break
    
    assert correo_encontrado, "No se encontró el correo de lista de espera para el ciudadano"

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
    # Verificar que hay al menos un correo en la bandeja de salida
    assert len(mail.outbox) > 0, "No se envió ningún correo"
    
    # Buscar el correo enviado al ciudadano promovido
    correo_encontrado = False
    for email in mail.outbox:
        if context.ciudadano_espera.correo_electronico in email.to:
            correo_encontrado = True
            # Verificar que es un correo de confirmación de inscripción
            assert "confirmación" in email.subject.lower(), "El asunto no indica que es una confirmación"
            assert context.evento.nombre_evento in email.subject, "El asunto no contiene el nombre del evento"
            break
    
    assert correo_encontrado, "No se encontró el correo de confirmación para el ciudadano promovido"
