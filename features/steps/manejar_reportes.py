"""
Este módulo contiene los pasos definidos para las pruebas de comportamiento
utilizando Behave. Se encarga de verificar la correcta asignación,
priorización y manejo de reportes en los departamentos municipales.

"""

from behave import *

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.reporte.reporte import Reporte
from ciudadano_app.models.reporte.tipo_reporte import TipoReporte
from entidad_municipal_app.models.reporte.reporte_municipal import ReporteMunicipal
from entidad_municipal_app.models.departamento.gestor_de_departamentos_y_reportes import GestorDeDepartamentosYReportes

#     Escenario: Resolver reportes asignados a un departamento

@step('nuevos reportes que llegan al gestor de departamentos')
def step_impl(context):
    """
    Inicializa el gestor de departamentos y obtiene los reportes municipales.

    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    context.gestor_de_departamentos_y_reportes = GestorDeDepartamentosYReportes()

    #Para obtener datos del escenario
    for row in context.table:
        # Crear ciudadano
        context.ciudadano, created = Ciudadano.objects.get_or_create(
            nombre_completo=row["nombre"],
            correo_electronico=row["correo"],
            numero_identificacion=row["identificacion"]
        )

        # Crear tipo de reporte
        tipo_reporte, created = TipoReporte.objects.get_or_create(
            asunto=row["asunto"],
            descripcion=row["descripcion"]
        )

        # Crear reporte
        reporte_ciudadano = Reporte.objects.create(
            ciudadano=context.ciudadano,
            tipo_reporte=tipo_reporte,
            ubicacion=row["ubicacion"]
        )

        # Crear reporte municipal
        ReporteMunicipal.objects.create(
            reporte_ciudadano=reporte_ciudadano, estado="asignado", evidencia=""
        )

    context.reportes_municipales = context.gestor_de_departamentos_y_reportes.obtener_reportes_municipales()

    assert context.reportes_municipales, "No hay reportes municipales disponibles."


@step('los reportes han sido asignados automáticamente a un departamento')
def step_impl(context):
    """
    Verifica que cada reporte municipal ha sido asignado a un departamento.

    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    for reporte in context.reportes_municipales:
        assert reporte.obtener_departamento() is not None, \
            f"El reporte {reporte.obtener_id()} no ha sido asignado a ningún departamento."


@step('los reportes son priorizados por su asunto')
def step_impl(context):
    """
    Verifica que los reportes tengan un nivel de prioridad asignado.

    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    for reporte in context.reportes_municipales:
        assert reporte.obtener_prioridad() > 0, \
            f"La prioridad del reporte {reporte.obtener_id()} no se ha calculado correctamente."


@step('el departamento "{nombre_departamento}" atienda el reporte "{id_reporte_atendido}"')
def step_impl(context, nombre_departamento, id_reporte_atendido):
    """
    Simula que un departamento atiende un reporte específico.

    :param nombre_departamento: Nombre del departamento encargado del reporte.
    :type nombre_departamento: str
    :param id_reporte_atendido: ID del reporte a atender.
    :type id_reporte_atendido: str
    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    context.departamento = context.gestor_de_departamentos_y_reportes.obtener_departamento_por_nombre(nombre_departamento)
    context.reporte_atendido = context.gestor_de_departamentos_y_reportes.obtener_reporte_municipal_por_id(id_reporte_atendido)

    context.departamento.atender_reporte_municipal(context.reporte_atendido)

    assert context.reporte_atendido.obtener_estado() == "atendiendo", \
        f"El reporte {context.reporte_atendido.obtener_id()} no está siendo atendido."


@step("el departamento registra la evidencia {descripcion_evidencia} de la solución del reporte atendido")
def step_impl(context, descripcion_evidencia):
    """
    Registra la evidencia de la solución de un reporte atendido.

    :param descripcion_evidencia: Descripción de la evidencia.
    :type descripcion_evidencia: str
    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    context.reporte_atendido.registrar_evidencia(descripcion_evidencia)

    assert context.reporte_atendido.obtener_evidencia() != "", \
        f"El reporte {context.reporte_atendido.obtener_id()} no tiene evidencia registrada."


@step('el estado del reporte atendido cambia a "resuelto"')
def step_impl(context):
    """
    Verifica que el estado del reporte atendido cambie a "resuelto".

    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    assert context.reporte_atendido.obtener_estado() == "resuelto", \
        f"El estado del reporte {context.reporte_atendido.obtener_id()} no se actualizó correctamente."

#   Escenario: Resolver reportes postergados de un departamento

@step('el departamento "{nombre_departamento}" posterga el reporte "{id_reporte_postergado}"')
def step_impl(context, nombre_departamento, id_reporte_postergado):
    """
    Simula la postergación de un reporte por parte de un departamento.

    :param nombre_departamento: Nombre del departamento encargado del reporte.
    :type nombre_departamento: str
    :param id_reporte_postergado: ID del reporte a postergar.
    :type id_reporte_postergado: str
    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    context.departamento = context.gestor_de_departamentos_y_reportes.obtener_departamento_por_nombre(nombre_departamento)
    context.reporte_postergado = context.gestor_de_departamentos_y_reportes.obtener_reporte_municipal_por_id(id_reporte_postergado)

    context.departamento.postergar_reporte(context.reporte_postergado)

    assert context.reporte_postergado.obtener_estado() == "postergado", \
        f"El estado del reporte {context.reporte_postergado.obtener_id()} no se actualizó correctamente."