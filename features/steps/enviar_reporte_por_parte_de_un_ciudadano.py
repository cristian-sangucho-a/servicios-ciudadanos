from behave import *

from ciudadano_app.models import *
from ciudadano_app.models.ServicioDeReporte import ServicioDeReporte
from mocks.RepositorioDeReporteEnMemoria import RepositorioDeReporteEnMemoria, generar_registros

repositorioEnMemoria = RepositorioDeReporteEnMemoria()
servicioDeReporte = ServicioDeReporte(repositorioEnMemoria)

@step(
    'que un ciudadano llamado "{nombre}" con correo "{correo}" e identificación "{identificacion}" ha identificado un problema')
def step_impl(context, nombre, correo, identificacion):
    context.ciudadano = Ciudadano(nombre=nombre, correo=correo, identificacion=identificacion)

@step(
    'proporciona sus detalles en un reporte con asunto "{asunto}", descripción "{descripcion}" y ubicación "{ubicacion}"')
def step_impl(context, asunto, descripcion, ubicacion):
    tipo_reporte = TipoReporte(asunto=asunto, descripcion=descripcion)
    context.tipo_reporte = tipo_reporte
    context.reporte = Reporte(ciudadano=context.ciudadano, tipo_reporte=tipo_reporte, ubicacion=ubicacion)

@step("se envía el reporte descrito")
def step_impl(context):
    servicioDeReporte.enviar_reporte(context.reporte)

@step('se asigna una prioridad de acuerdo a "{cantidad_registro}" registros previos del problema con asunto "{asunto}"')
def step_impl(context, cantidad_registro, asunto):
    generar_registros(repositorioEnMemoria, cantidad_registro, asunto)
    context.reporte = servicioDeReporte.priorizar(context.reporte)

@step('el reporte es asignado con prioridad "{prioridad_esperada}"')
def step_impl(context, prioridad_esperada):
    assert int(prioridad_esperada) == context.reporte.prioridad
