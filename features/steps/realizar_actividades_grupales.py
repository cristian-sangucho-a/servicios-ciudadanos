from unittest.mock import Mock, patch
from behave import *
from faker import Faker
from datetime import datetime

from ciudadano_app.models.area_comunal import AreaComunal
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.servicio_reserva import ServicioReserva
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from mocks.repositorio_reserva_en_memoria import RepositorioReservaMemoria

fake = Faker()

servicio_reserva_en_memoria = RepositorioReservaMemoria()
servicio_reserva=ServicioReserva()


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
        area.id = ++index
        # area.id = fake.random_number(digits=3)
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

    # Simular que tiene 0 reservas (ajusta según tu lógica)
    servicio_reserva_en_memoria.reservas_ciudadano_list = []

    assert len(servicio_reserva_en_memoria.reservas_ciudadano_list) < int(maximo_reservas)

@step(
    'el ciudadano realice una reserva "{tipo_reserva}" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, tipo_reserva, area_comunal, fecha_reserva, hora_inicio, hora_fin):
    context.tipo_reserva = tipo_reserva
    context.fecha_reserva = fecha_reserva
    context.hora_inicio = hora_inicio
    context.hora_fin = hora_fin

    pass

@step("se guarda la reserva en la Agenda Pública")
def step_impl(context):
    id_reserva, reservado = servicio_reserva_en_memoria.reservar_area_comunal(
        area_comunal= servicio_reserva_en_memoria.obtener_area_comunal(1),
        fecha_reserva=context.fecha_reserva,
        hora_inicio=context.hora_inicio,
        hora_fin=context.hora_fin,
        tipo_reserva=context.tipo_reserva,
        ciudadano=context.ciudadano
    ) ##SALTA ERROR AL MOMENTO DE RESERVAR ----- no hay que usar el modelo

    if context.correos_invitados:
        context.reserva = servicio_reserva_en_memoria.obtener_reserva_por_id(id_reserva=context.id_reserva)
        assert context.reserva.agregar_correos_invitados(correos_invitados=context.correos_invitados)
     #TODO: revisar si es necesario refactorar, como no hay agenda publica(en los modelos) el cuando y entonces sea uno solo

# ##########################FIN PRIMER ESCENARIO####################################
#
# @step('el ciudadano realice una reserva "privada" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
# def step_impl(context, area_comunal, fecha_reserva, hora_inicio, hora_fin):
#     context.tipo_reserva = "privada"
#     context.fecha_reserva = fecha_reserva
#     context.hora_inicio = hora_inicio
#     context.hora_fin = hora_fin
#     pass #da valor en el siguiente paso
#
@step('agregue los correos de los invitados "{correos_invitados}" a la reserva')
def step_impl(context, correos_invitados):
    context.correos_invitados = correos_invitados
    pass

@step("se enviará una invitación por correo con los detalles de la reserva.")
def step_impl(context):
    servicio_reserva_en_memoria.enviar_invitacion(context.reserva)
    pass


#
# #--------------------AQUI SE USA EL ENTONCES DE ARRIBA --------------------------#
#
# @step("se enviará una invitación por correo con los detalles de la reserva.")
# def step_impl(context):
#     context.controlador_notificacion = ControladorNotificacion()
#     assert context.controlador_notificacion.enviar_invitacion(reserva = context.ciudadano.obtener_reserva_por_id(id_reserva = context.id_reserva))
#
#     # Esta es una consideracion que me da deepsek para agilizar el tiempo que demora en enviarse un mensaje y arrojar algun codigo de OK
#     # from unittest.mock import patch
#     #
#     # @step("se enviará una invitación por correo...")
#     # def step_impl(context):
#     #     with patch('app.models.ControladorNotificacion.enviar_invitacion') as mock:
#     #         context.reserva.notificar_invitados()
#     #         assert mock.called
#
#
# ##########################FIN SEGUNDO ESCENARIO####################################
#
#
@step(
     'que el ciudadano tiene una reserva "publica" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):
     context.id_reserva, reservado = servicio_reserva_en_memoria.reservar_area_comunal(
         area_comunal=servicio_reserva_en_memoria.obtener_area_comunal(2),
         fecha_reserva=context.fecha_reserva,
         hora_inicio=context.hora_inicio,
         hora_fin=context.hora_fin,
         tipo_reserva="publica",
         ciudadano=context.ciudadano
     )
     assert servicio_reserva_en_memoria.obtener_reserva_por_id(context.id_reserva)['tipo_reserva'] == "publica" #se verifica que tiene la reserva

@step("cancele la reserva")
def step_impl(context):
    pass
    #assert servicio_reserva_en_memoria.cancelar_reserva(id_reserva=context.id_reserva, ciudadano=context.ciudadano) #verificar

@step("la reserva será eliminada de la agenda pública.")
def step_impl(context):
    assert context.controlador_reserva.cancelar_reserva(id_reserva=context.id_reserva, ciudadano=context.ciudadano2) #verificar que se calcelo con un TRUE

##########################FIN TERCER ESCENARIO####################################
@step(
    'que el ciudadano tiene una reserva "privada" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):
    context.id_reserva, context.reservado = context.controlador_reserva.reservar_area_comunal(
        area_comunal=context.cancha3,
        fecha_reserva=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        tipo_reserva="privada",
        ciudadano=context.ciudadano2
    )
    #assert context.reservado #se verifica que tiene la reserva
    pass

@step("se enviará una correo de cancelacion a los invitados")
def step_impl(context):
    #assert context.controlador_notificacion.enviar_cancelacion(
        #id_reserva=context.ciudadano.obtener_reserva_por_id(id_reserva=context.id_reserva))
    pass