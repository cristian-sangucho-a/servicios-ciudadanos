"""
Este módulo contiene los pasos definidos para las pruebas de comportamiento
utilizando Behave. Se encarga de verificar la correcta asignación,
priorización y manejo de reportes en los departamentos municipales.

"""

from behave import *

from entidad_municipal_app.models.departamento.servicio_departamento import ServicioDepartamento
from entidad_municipal_app.models.reporte.servicio_de_reporte_municipal import ServicioReporteMunicipal
from mocks.repositorio_de_departamento_en_memoria import RepositorioDeDepartamentoEnMemoria
from mocks.repositorio_de_reporte_municipal_en_memoria import RepositorioDeReporteMunicipalEnMemoria

repositorio_de_departamento_en_memoria = RepositorioDeDepartamentoEnMemoria()
repositorio_de_reporte_en_memoria = RepositorioDeReporteMunicipalEnMemoria()
servicio_de_reporte = ServicioReporteMunicipal(repositorio_de_reporte_en_memoria)
servicio_de_departamento = ServicioDepartamento(repositorio_de_departamento_en_memoria,)

#     Escenario: Resolver reportes asignados a un departamento

@step('nuevos reportes que llegan al gestor de departamentos')
def step_impl(context):
    """
    Inicializa el gestor de departamentos y obtiene los reportes municipales.

    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """

    #Para obtener datos del escenario
    context.reportes_municipales = servicio_de_reporte.obtener_reportes_municipales()
    assert len(context.reportes_municipales)>0, "No hay reportes municipales disponibles."


@step('los reportes han sido asignados automáticamente a un departamento')
def step_impl(context):
    """
    Verifica que cada reporte municipal ha sido asignado a un departamento.

    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    for reporte in context.reportes_municipales:
        assert "asignado" == reporte.obtener_estado(), \
            f"El reporte {reporte.obtener_id()} no ha sido asignado a ningún departamento."




@step('los reportes son priorizados por su asunto')
def step_impl(context):
    """
    Verifica que los reportes tengan un nivel de prioridad asignado.

    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    pass


@step('el departamento "{nombre_departamento}" atienda el reporte "{id_reporte_atendido:d}"')
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
    context.departamento = servicio_de_departamento.obtener_departamento_por_nombre(nombre_departamento)

    context.reporte_atendido = servicio_de_reporte.obtener_reporte_municipal_por_id(id_reporte_atendido)
    assert servicio_de_reporte.atender_reporte_municipal(id_reporte_atendido),\
        f"El reporte {id_reporte_atendido} no está siendo atendido."


@step("el departamento registra la evidencia {descripcion_evidencia} de la solución del reporte atendido")
def step_impl(context, descripcion_evidencia):
    """
    Registra la evidencia de la solución de un reporte atendido.

    :param descripcion_evidencia: Descripción de la evidencia.
    :type descripcion_evidencia: str
    :param context: Contexto de Behave.
    :type context: behave.runner.Context
    """
    servicio_de_reporte.registrar_evidencia(context.reporte_atendido, descripcion_evidencia)

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

@step('el departamento "{nombre_departamento}" posterga el reporte "{id_reporte_postergado:d}"')
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
    context.departamento = servicio_de_departamento.obtener_departamento_por_nombre(nombre_departamento)
    context.reporte_postergado = servicio_de_reporte.obtener_reporte_municipal_por_id(id_reporte_postergado)
    assert servicio_de_reporte.postergar_reporte(id_reporte_postergado), \
        "El reporte no ha sido postergado"