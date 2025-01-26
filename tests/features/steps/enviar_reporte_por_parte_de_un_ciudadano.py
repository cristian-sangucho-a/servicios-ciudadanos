from behave import *

from ciudadano_app.models import Ciudadano
from ciudadano_app.models.Reporte import Reporte
from ciudadano_app.models.ServicioDeReporte import ServicioDeReporte
from ciudadano_app.models.TipoReporte import TipoReporte
from tests.mocks.RepositorioDeReporteEnMemoria import RepositorioDeReporteEnMemoria, generar_registros

repositorioEnMemoria = RepositorioDeReporteEnMemoria()
servicioDeReporte = ServicioDeReporte(repositorioEnMemoria)

@step(
    'que un ciudadano llamado "{nombre}" con correo "{correo}" e identificación "{identificacion}" ha identificado un problema')
def step_impl(context, nombre, correo, identificacion):
    context.ciudadano = Ciudadano(nombre, correo, identificacion)


@step(
    'proporciona sus detalles en un reporte con asunto "{asunto}", descripción "{descripcion}" y ubicación "{ubicacion}"')
def step_impl(context, asunto, descripcion, ubicacion):
    context.tipo_reporte = TipoReporte(asunto, descripcion)
    context.reporte = Reporte(context.ciudadano, context.tipo_reporte, ubicacion=ubicacion)

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
