from unittest.mock import Mock, patch
from behave import *
from faker import Faker
from datetime import datetime

from ciudadano_app.admin import AreaComunal
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from mocks.repositorio_reserva_en_memoria import RepositorioReservaMemoria

fake = Faker()

servicio_reserva_en_memoria = RepositorioReservaMemoria()

@step('que existen areas comunales disponibles en el espacio publico "{nombre_espacio_publico}" en la ciudad y son')
def step_impl(context, nombre_espacio_publico):
    # Create mock objects instead of real database objects
    context.entidad_municipal = EntidadMunicipal(nombre="Municipio de Quito")
    context.espacio_publico = EspacioPublico(nombre=nombre_espacio_publico, entidad_municipal=context.entidad_municipal)

    context.cancha1 = AreaComunal()
    context.cancha2 = AreaComunal()
    context.cancha3 = AreaComunal()

    # Set up the mock areas with their names from the table
    context.cancha1.nombre_area = context.table[0].cells[0]
    context.cancha2.nombre_area = context.table[1].cells[0]
    context.cancha3.nombre_area = context.table[2].cells[0]

    context.espacio_publico.areas_comunales = [context.cancha1, context.cancha2, context.cancha3]
    # Set up mock behaviors
    assert servicio_reserva_en_memoria.hay_areas_comunales_disponibles(espacio_publico=context.espacio_publico)

#
# @step('el ciudadano no supera las "{maximo_reservas}" reservas activas')
# def step_impl(context, maximo_reservas):
#     # Create mock citizen instead of database object
#     context.ciudadano = Mock()
#     context.ciudadano.correo_electronico = fake.email()
#     context.ciudadano.nombre_completo = fake.name()
#     context.ciudadano.numero_identificacion = str(fake.random_number(digits=10))
#
#     # Create mock reservation service
#     context.servicio_reserva = Mock()
#     context.servicio_reserva.ciudadano_supera_maximo_reservas.return_value = False
#
#     # Verify the maximum reservas condition
#     assert int(maximo_reservas) >= 0
#     context.maximo_reservas = int(maximo_reservas)
#
#
# @step(
#     'el ciudadano realice una reserva "{tipo_reserva}" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
# def step_impl(context, tipo_reserva, area_comunal, fecha_reserva, hora_inicio, hora_fin):
#     context.tipo_reserva = tipo_reserva
#     context.fecha_reserva = fecha_reserva
#     context.hora_inicio = hora_inicio
#     context.hora_fin = hora_fin
#
#     # Store the requested area
#     context.area_solicitada = next(
#         area for area in [context.cancha1, context.cancha2, context.cancha3]
#         if area.nombre_area == area_comunal
#     )
#
#
# @step("se guarda la reserva en la Agenda Pública")
# def step_impl(context):
#     # Mock the reservation service
#     context.servicio_reserva = Mock()
#     context.servicio_reserva.reservar_area_comunal.return_value = (1, True)  # (id_reserva, reservado)
#
#     # Attempt reservation
#     context.id_reserva, context.reservado = context.servicio_reserva.reservar_area_comunal(
#         area_comunal=context.area_solicitada,
#         fecha_reserva=context.fecha_reserva,
#         hora_inicio=context.hora_inicio,
#         hora_fin=context.hora_fin,
#         tipo_reserva=context.tipo_reserva,
#         ciudadano=context.ciudadano
#     )
#
#     # Verify the reservation was successful
#     assert context.reservado
#     assert context.id_reserva > 0
#     # TODO: revisar si es necesario refactorar, como no hay agenda publica(en los modelos) el cuando y entonces sea uno solo

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
# @step('agregue los correos de los invitados "{correos_invitados}" a la reserva')
# def step_impl(context, correos_invitados):
#     assert context.controlador_reserva.obtener_reserva_por_id(id_reserva = context.id_reserva).agregar_correos_invitados(correos_invitados = correos_invitados)
#     # esto puede ser verificado en el siguiente paso o no xd
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
# @step(
#     'que el ciudadano tiene una reserva "publica" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
# def step_impl(context, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):
#     context.ciudadano2 = Ciudadano.objects.create_user(
#         correo_electronico=fake.email(),
#         nombre_completo=fake.name(),
#         numero_identificacion=str(fake.random_number(digits=10)),
#         contrasena="secret122"
#     )
#
#     context.id_reserva, context.reservado = context.controlador_reserva.reservar_area_comunal(
#         area_comunal=context.cancha3,
#         fecha_reserva=fecha,
#         hora_inicio=hora_inicio,
#         hora_fin=hora_fin,
#         tipo_reserva="publica",
#         ciudadano=context.ciudadano2
#     )
#     #assert context.reservado #se verifica que tiene la reserva
#     pass
#
# @step("cancele la reserva")
# def step_impl(context):
#     pass
#
# @step("la reserva será eliminada de la agenda pública.")
# def step_impl(context):
#     #assert context.controlador_reserva.cancelar_reserva(id_reserva=context.id_reserva, ciudadano=context.ciudadano2) #verificar que se calcelo con un TRUE
#     pass
# ##########################FIN TERCER ESCENARIO####################################
#
# @step(
#     'que el ciudadano tiene una reserva "privada" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
# def step_impl(context, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):
#     context.id_reserva, context.reservado = context.controlador_reserva.reservar_area_comunal(
#         area_comunal=context.cancha3,
#         fecha_reserva=fecha,
#         hora_inicio=hora_inicio,
#         hora_fin=hora_fin,
#         tipo_reserva="privada",
#         ciudadano=context.ciudadano2
#     )
#     #assert context.reservado #se verifica que tiene la reserva
#     pass
# @step("se enviará una correo de cancelacion a los invitados")
# def step_impl(context):
#     #assert context.controlador_notificacion.enviar_cancelacion(
#         #id_reserva=context.ciudadano.obtener_reserva_por_id(id_reserva=context.id_reserva))
#     pass