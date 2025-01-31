from behave import *
from faker import Faker
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models.ciudad.sector import Sector
from shared.models.reporte.reporte import Reporte
from shared.models.notificacion.servicio_de_notificacion import ServicioDeNotificacion

# use_step_matcher("re")

fake = Faker()


# Escenario: Seleccionar sector de interés
@step('que existen sectores en la ciudad y son')
def step_impl(context):
    context.sectores = []
    for row in context.table:
        context.sectores.append(Sector(nombre=row['nombre_sector']))


@step('el ciudadano "{nombre_ciudadano}" seleccione "{nombre_sector}" como sector de interés')
def step_impl(context, nombre_ciudadano, nombre_sector):
    context.ciudadano = Ciudadano(nombre=nombre_ciudadano)
    sector = next((s for s in context.sectores if s.nombre == nombre_sector), None)
    context.ciudadano.agregar_sector_de_interes(sector)


@step('se agregará a la lista de sectores de interés')
def step_impl(context):
    assert len(context.ciudadano.sectores_de_interes) == 1


# Escenario: Notificar un reporte de alta prioridad en un sector de interés
@step('que el ciudadano "{nombre_ciudadano}" tiene registrado "{nombre_sector}" como sector de interés')
def step_impl(context, nombre_ciudadano, nombre_sector):
    context.ciudadano = Ciudadano(nombre=nombre_ciudadano)
    context.sector = Sector(nombre=nombre_sector)
    context.ciudadano.agregar_sector_de_interes(context.sector)


@step('se registre un reporte con asunto "{asunto}"')
def step_impl(context, asunto):
    context.reporte = Reporte(asunto=asunto, sector=context.ciudadano.sectores_de_interes[0])
    context.notificador = ServicioDeNotificacion()
    context.notificador.notificar_reporte(context.ciudadano, context.reporte)


@step('el estado del reporte no es "Resuelto"')
def step_impl(context):
    assert context.report.status != "Resuelto"


@step('se enviará un correo con los detalles del reporte')
def step_impl(context):
    servicio_de_notificaciones = ServicioDeNotificacion()
    servicio_de_notificaciones.notificar(context.ciudadano, context.reporte)


@step("se agregará a la lista de notificaciones")
def step_impl(context):
    assert len(context.ciudadano.notificaciones) == 1


# Escenario: Notificar un reporte reportado en un sector cercano a mi ubicación actual
@step('que el ciudadano "{nombre_ciudadano}" se encuentra en el sector "{nombre_sector}"')
def step_impl(context, nombre_ciudadano, nombre_sector):
    context.ciudadano = Ciudadano(nombre=nombre_ciudadano)
    sector = Sector(nombre=nombre_sector)
    context.ciudadano.actualizar_ubicacion(sector)
    context.sector = sector


@step('se registre un reporte con asunto "{asunto}" a menos de {distancia} kilómetros de su ubicación actual')
def step_impl(context, asunto, distancia):
    sector_cercano = Sector(nombre=fake.city())
    context.reporte = Reporte(tipo=asunto, sector=sector_cercano)
    context.notificador = ServicioDeNotificacion()
    context.notificador.notificar_reporte_cercano(context.ciudadano, context.reporte, float(distancia))


# Escenario: Notificar cuando el estado de un sector de interés sea de riesgo
@step('se registren al menos "{cantidad}" reportes con asunto "{asunto}"')
def step_impl(context, cantidad, asunto):
    for _ in range(int(cantidad)):
        Reporte(tipo=asunto, sector=context.sector)
    context.notificador = ServicioDeNotificacion()
    context.notificador.notificar_estado_riesgo(context.ciudadano, context.sector)


@step('el sector cambiará a estado "Riesgo"')
def step_impl(context):
    assert context.sector.estado == "Riesgo"


@step('se enviará un correo con el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    assert mensaje in context.notificador.ultima_notificacion
