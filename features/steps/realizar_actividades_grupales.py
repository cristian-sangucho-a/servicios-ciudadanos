from unittest.mock import Mock, patch
from behave import step
from faker import Faker
from datetime import datetime
from ciudadano_app.models.area_comunal import AreaComunal
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from mocks.repositorio_reserva_en_memoria import RepositorioReservaMemoria

fake = Faker()
servicio_reserva_en_memoria = RepositorioReservaMemoria()


@step('que existen areas comunales disponibles en el espacio publico "{nombre_espacio_publico}" en la ciudad y son')
def step_impl(context, nombre_espacio_publico):
    context.entidad_municipal = EntidadMunicipal(
        nombre="Municipalidad Mock",
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email(),
        fecha_registro=datetime.now()
    )
    context.entidad_municipal.id = 1

    context.espacio_publico = EspacioPublico(
        nombre=nombre_espacio_publico,
        entidad_municipal=context.entidad_municipal
    )
    context.espacio_publico.id = 1

    index = 1

    for row in context.table:
        area = AreaComunal(
            nombre_area=row['Nombre'],
            hora_de_apertura=datetime.strptime("08:00", "%H:%M").time(),
            hora_de_cierre=datetime.strptime("20:00", "%H:%M").time(),
            espacio_publico=context.espacio_publico
        )
        area.id = index
        index += 1
        servicio_reserva_en_memoria.agregar_area_comunal(area, context.espacio_publico)

    assert servicio_reserva_en_memoria.hay_areas_comunales_disponibles(context.espacio_publico)


@step('el ciudadano no supera las "{maximo_reservas}" reservas activas')
def step_impl(context, maximo_reservas):
    context.ciudadano = Ciudadano(
        nombre_completo=fake.name(),
        correo_electronico=fake.email(),
        numero_identificacion=str(fake.random_number(digits=10)),
        esta_activo=True
    )
    context.ciudadano.id = 1
    context.maximo_reservas = int(maximo_reservas)
    assert not servicio_reserva_en_memoria.ciudadano_supera_maximo_reservas(ciudadano=context.ciudadano)


@step(
    'el ciudadano realice una reserva "{tipo_reserva}" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, tipo_reserva, area_comunal, fecha_reserva, hora_inicio, hora_fin):
    context.tipo_reserva = tipo_reserva
    context.fecha_reserva = fecha_reserva
    context.hora_inicio = hora_inicio
    context.hora_fin = hora_fin
    context.correos_invitados = None


@step("se guarda la reserva en la Agenda Pública")
def step_impl(context):
    context.id_reserva, reservado = servicio_reserva_en_memoria.reservar_area_comunal(
        area_comunal=servicio_reserva_en_memoria.obtener_area_comunal(1),
        fecha_reserva=context.fecha_reserva,
        hora_inicio=context.hora_inicio,
        hora_fin=context.hora_fin,
        tipo_reserva=context.tipo_reserva,
        ciudadano=context.ciudadano
    )

    if context.correos_invitados is not None:
        servicio_reserva_en_memoria.agregar_correos_invitados_a_reserva(id_reserva=context.id_reserva,
                                                                        correos_invitados=context.correos_invitados)
    assert reservado

@step('agregue los correos de los invitados "{correos_invitados}" a la reserva')
def step_impl(context, correos_invitados):
    context.correos_invitados = correos_invitados


@step("se enviará una invitación por correo con los detalles de la reserva.")
def step_impl(context):
    assert servicio_reserva_en_memoria.enviar_invitacion(
        servicio_reserva_en_memoria.obtener_reserva_por_id(context.id_reserva))


@step(
    'que el ciudadano tiene una reserva "{tipo_reserva}" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, tipo_reserva, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):

    crear_contexto_para_la_reserva(context, nombre_espacio)

    context.id_reserva, reservado = servicio_reserva_en_memoria.reservar_area_comunal(
        area_comunal=servicio_reserva_en_memoria.obtener_area_comunal(1),
        fecha_reserva=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        tipo_reserva=tipo_reserva,
        ciudadano=context.ciudadano
    )

    context.correos_invitados = "jean.cotera@epn.edu.ec, jorman.chuquer@epn.edu.ec"

    if tipo_reserva == "privada":
        servicio_reserva_en_memoria.agregar_correos_invitados_a_reserva(id_reserva=context.id_reserva,
                                                                        correos_invitados=context.correos_invitados)

    assert reservado





@step("cancele la reserva")
def step_impl(context):
    pass # Da valor en el siguiente paso

@step("la reserva será eliminada de la agenda pública.")
def step_impl(context):
    assert servicio_reserva_en_memoria.cancelar_reserva(id_reserva=context.id_reserva,
                                                        ciudadano=context.ciudadano)  # verificar que se calcelo con un TRUE


@step("se enviará una correo de cancelacion a los invitados")
def step_impl(context):
    assert servicio_reserva_en_memoria.enviar_cancelacion(servicio_reserva_en_memoria.obtener_reserva_por_id(context.id_reserva))

def crear_contexto_para_la_reserva(context, nombre_espacio):
    context.entidad_municipal = EntidadMunicipal(
        nombre="Municipalidad Mock",
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email(),
        fecha_registro=datetime.now()
    )
    context.entidad_municipal.id = 1
    context.espacio_publico = EspacioPublico(
        nombre=nombre_espacio,
        entidad_municipal=context.entidad_municipal
    )
    context.espacio_publico.id = 1
    index = 1
    for _ in range(0, 3):
        area = AreaComunal(
            nombre_area=fake.word(),
            hora_de_apertura=datetime.strptime("08:00", "%H:%M").time(),
            hora_de_cierre=datetime.strptime("20:00", "%H:%M").time(),
            espacio_publico=context.espacio_publico
        )
        index += 1
        area.id = index
        servicio_reserva_en_memoria.agregar_area_comunal(area, context.espacio_publico)
    context.ciudadano = Ciudadano(
        nombre_completo=fake.name(),
        correo_electronico=fake.email(),
        numero_identificacion=str(fake.random_number(digits=10)),
        esta_activo=True
    )
    context.ciudadano.id = 1