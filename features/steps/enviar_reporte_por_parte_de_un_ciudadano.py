from behave import step

from ciudadano_app.models import Ciudadano
from shared.models import TipoReporte, Reporte
from shared.models import ServicioDeReporte

from mocks.repositorio_de_reporte_en_memoria import (
    RepositorioDeReporteEnMemoria,
    generar_registros,
)

repositorioEnMemoria = RepositorioDeReporteEnMemoria()
servicioDeReporte = ServicioDeReporte(repositorioEnMemoria)

@step(
    'que un ciudadano llamado "{nombre}" con correo "{correo}" e identificación "{identificacion}" ha identificado un problema'
)
def step_impl(context, nombre, correo, identificacion):
    context.ciudadano = Ciudadano(
        nombre_completo=nombre, correo_electronico=correo, numero_identificacion=identificacion
    )


@step(
    'proporciona sus detalles en un reporte con asunto "{asunto}", descripción "{descripcion}" y ubicación "{ubicacion}"'
)
def step_impl1(context, asunto, descripcion, ubicacion):
    tipo_reporte = TipoReporte(asunto=asunto, descripcion=descripcion)
    context.tipo_reporte = tipo_reporte
    context.reporte = Reporte(
        ciudadano=context.ciudadano, tipo_reporte=tipo_reporte, ubicacion=ubicacion
    )


@step("se envía el reporte descrito")
def step_impl2(context):
    servicioDeReporte.enviar_reporte(context.reporte)


@step(
    'se asigna una prioridad de acuerdo a "{cantidad_registro}" registros previos del problema con asunto "{asunto}"'
)
def step_impl3(context, cantidad_registro, asunto):
    generar_registros(repositorioEnMemoria, cantidad_registro, asunto)
    context.reporte = servicioDeReporte.priorizar(context.reporte)


@step('el reporte es asignado con prioridad "{prioridad_esperada}"')
def step_impl4(context, prioridad_esperada):
    assert int(prioridad_esperada) == context.reporte.prioridad


@step(
    'que un ciudadano llamado "{nombre}" con correo "{correo}" e identificación "{identificacion}" visualice el reporte con asunto "{asunto}" y ubicación "{ubicacion}"'
)
def step_impl(context, nombre, correo, identificacion, asunto, ubicacion):
    context.ciudadano = Ciudadano(
        nombre_completo=nombre, correo_electronico=correo, numero_identificacion=identificacion
    )
    context.reporte = Reporte(
        ciudadano=context.ciudadano,
        tipo_reporte=TipoReporte(asunto=asunto),
        ubicacion=ubicacion,
    )


@step('el reporte cuente con "{cantidad_registro}" de registros previos de dicho reporte y prioridad "{prioridad}"')
def step_impl1(context, cantidad_registro, prioridad):
    generar_registros(repositorioEnMemoria, cantidad_registro, context.reporte.tipo_reporte.asunto)
    context.reporte = servicioDeReporte.priorizar(context.reporte)
    assert int(prioridad) == context.reporte.prioridad


@step("se confirma el reporte")
def step_impl2(context):
    servicioDeReporte.confirmar_reporte(context.reporte)


@step('se crea un nuevo reporte con el mismo "{asunto}", "{ubicacion}" y "{descripcion}"')
def step_impl3(context, asunto, ubicacion, descripcion):
    tipo_reporte = TipoReporte(asunto=asunto, descripcion=descripcion)
    context.reporte = Reporte(
        ciudadano=context.ciudadano, tipo_reporte=tipo_reporte, ubicacion=ubicacion
    )