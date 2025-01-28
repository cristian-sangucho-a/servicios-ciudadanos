"""
Este módulo contiene los pasos definidos para las pruebas de comportamiento
utilizando Behave.
"""
from behave import *

from entidad_municipal_app.models.reporte.reporte import Reporte
from entidad_municipal_app.models.departamento.departamento import Departamento
from entidad_municipal_app.models.departamento.gestor_de_departamentos_y_reportes import GestorDeDepartamentos

#use_step_matcher("re")

#Escenario 1.1
@step('los siguientes reportes ciudadanos llegan al gestor de departamentos')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.gestor_de_departamentos = GestorDeDepartamentos()

    context.gestor_de_departamentos = GestorDeDepartamentos()
    for row in context.table:
        reporte = Reporte(row["id_reporte"], row["descripcion_reporte"])
        context.gestor_de_departamentos.agregar_nuevo_reporte_no_asignado(reporte)
    pass



@step('los reportes han sido asignados automáticamente a un departamento')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """

    context.gestor_de_departamentos.asignar_automaticamente_reportes_a_departamentos()
    pass


@step('el departamento "{nombre_departamento}" priorice los reportes asignados')
def step_impl(context, nombre_departamento):
    """
    :type nombre_departamento: str
    :type context: behave.runner.Context
    """
    context.departamento = context.gestor_de_departamentos.obtener_departamento_por_nombre(nombre_departamento)
    context.departamento.priorizar_reportes()
    pass


@step('el departamento atienda el reporte "{id_reporte_atendido}"')
def step_impl(context, id_reporte_atendido):
    """
    :type id_reporte_atendido: str
    :type id_reporte_atendido: str
    :type context: behave.runner.Context
    """
    context.reporte_atendido = context.departamento.obtener_reporte_por_id(id_reporte_atendido)
    context.departamento.atender_reporte(context.reporte_atendido)
    assert "atendiendo" == context.reporte_atendido.obtener_estado() , "El reporte no está siendo atendido"


@step("el departamento registra la evidencia {descripcion_evidencia} de la solución del reporte atendido")
def step_impl(context, descripcion_evidencia):
    """
    :type descripcion_evidencia: str
    :type context: behave.runner.Context
    """
    context.departamento.registrar_evidencia(context.reporte_atendido, descripcion_evidencia)
    assert "" != context.reporte_atendido.obtener_evidencia(), \
        "El reporte {context.reporte_atendido.obtener_id()} no tiene la evidencia registrada."


@step('el estado del reporte atendido cambia a "resuelto"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    context.reporte_atendido.cambiar_estado("resuelto")
    assert context.reporte_atendido.obtener_estado() == "resuelto", \
        f"El estado del reporte {context.reporte_atendido.obtener_id()} no se actualizó correctamente."

#Escenario 2.1
@step('el departamento "{nombre_departamento}" posterga el reporte "{id_reporte_postergado}"')
def step_impl(context, nombre_departamento, id_reporte_postergado):
    """
    :param nombre_departamento:
    :type id_reporte_postergado: str
    :type context: behave.runner.Context
    """
    context.departamento = context.gestor_de_departamentos.obtener_departamento_por_nombre(nombre_departamento)
    context.reporte_postergado = context.departamento.obtener_reporte_por_id(id_reporte_postergado)
    context.departamento.postergar_reporte(context.reporte_postergado)
    assert context.reporte_postergado.obtener_estado() == "postergado", \
        f"El estado del reporte {context.reporte_postergado.obtener_id()} no se actualizó correctamente."


#Escenrio 3.1
@step('los reportes no han sido asignados a ningún departamento')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    reportes_no_asignados = context.gestor_de_departamentos.obtener_reportes_no_asignados()
    assert len(reportes_no_asignados) > 0, "Todos los reportes han sido asignados automáticamente."

@step('se realiza una asignación manual del reporte "{id_reporte}" al departamento "{departamento}"')
def step_impl(context, id_reporte, departamento):
    """
    :type id_reporte: str
    :type departamento: str
    :type context: behave.runner.Context
    """

    reporte_no_asignado = context.gestor_de_departamentos.obtener_reporte_por_id(id_reporte)

    departamento_destino = context.gestor_de_departamentos.obtener_departamento_por_nombre(departamento)

    if not departamento_destino:
        departamento_destino = Departamento(departamento)
        context.gestor_de_departamentos.agregar_departamento(departamento_destino)

    context.gestor_de_departamentos.asignar_manualmente_reporte_a_departamento(reporte_no_asignado, departamento_destino)
    context.departamento = departamento_destino
    context.reporte_asignado = reporte_no_asignado

    assert context.reporte_asignado in context.departamento.obtener_reportes_asignados(), \
    "El reporte no fue asignado correctamente al departamento."

@step('el estado del reporte asignado cambia a "asignado"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    assert context.reporte_asignado.obtener_estado() == "asignado", \
        f"El reporte {context.reporte_asignado.obtener_id()} no cambió a estado 'asignado'."

@step('se añaden los siguientes criterios de clasificación para el departamento asignado')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    criterios = [row["criterio"] for row in context.table]
    context.gestor_de_departamentos.agregar_criterios_clasificacion_por_departamento(context.departamento, criterios)
    for criterio in criterios:
        assert criterio in context.gestor_de_departamentos.obtener_criterios_clasificacion_por_departamento(context.departamento), \
            f"El criterio '{criterio}' no fue añadido correctamente al departamento '{context.departamento}'."