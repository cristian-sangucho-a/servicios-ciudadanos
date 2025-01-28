from faker import Faker
from django.db import models
from behave import *
from ciudadano_app.models import *
from ciudadano_app.models.controlador_notificacion import ControladorNotificacion
from ciudadano_app.models.controlador_reserva import ControladorReserva
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico


#use_step_matcher("re")
fake = Faker()

@step('que existen areas comunales en el espacio publico "{nombre_espacio_publico}" disponibles en la ciudad y son')
def step_impl(context, nombre_espacio_publico):
    #la entidad municipal se encarga de la creación de espacios públicos (preguntarle al profe si la parte administrativa está fuera del alcance)
    context.entidad_municipal = EntidadMunicipal.objects.create(nombre="QuitoDMQ") #saber que mas tiene el espacio publico con el otro team
    #TODO revisar el modelo de EspacioPublico, los campos necesarios para crearse
    context.espacio_publico = EspacioPublico.objects.create(nombre=nombre_espacio_publico)

    context.cancha1 = AreaComunal.objects.create(nombre_area=context.table[0].cells[0])
    context.cancha2 = AreaComunal.objects.create(nombre_area=context.table[1].cells[0])
    context.cancha3 = AreaComunal.objects.create(nombre_area=context.table[2].cells[0])
    ##Quien deberia crear areas comunales, espacios publicos y fechas disponibles debe ser la entidad municipal. Por ello, podemos crear con mocks estos datos
    context.espacio_publico.agregar_area_comunal(area_comunal=context.cancha1)
    context.espacio_publico.agregar_area_comunal(area_comunal=context.cancha2)
    context.espacio_publico.agregar_area_comunal(area_comunal=context.cancha3)

    context.cancha1.agregar_fecha_disponible(fecha="15/01/2024", hora_inicio="07:00", hora_fin="20:00")
    context.cancha2.agregar_fecha_disponible(fecha="15/01/2024", hora_inicio="07:00", hora_fin="20:00")
    context.cancha3.agregar_fecha_disponible(fecha="15/01/2024", hora_inicio="07:00", hora_fin="20:00")
    context.espacio_publico = context.entidad_municipal.crear_espacio_publico(espacio_publico=context.espacio_publico)
    #assert context.espacio_publico.hay_areas_comunales_disponibles();
    pass
@step('el ciudadano no supera las "{maximo_reservas}" reservas activas')
def step_impl(context, maximo_reservas):
    context.ciudadano = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret123"
    )

    #assert context.ciudadano.obtener_numero_reservas_activas() <= int(maximo_reservas)
    pass
@step('el ciudadano realice una reserva "publica" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, area_comunal, fecha_reserva, hora_inicio, hora_fin):
    context.tipo_reserva = "publica"
    context.fecha_reserva = fecha_reserva
    context.hora_inicio = hora_inicio
    context.hora_fin = hora_fin
    pass #da valor en el siguiente paso


@step("se guarda la reserva en la Agenda Pública")
def step_impl(context):
    context.controlador_reserva = ControladorReserva()
    context.id_reserva, context.reservado = context.controlador_reserva.reservar_area_comunal(
        area_comunal=context.cancha1,
        fecha_reserva=context.fecha_reserva,
        hora_inicio=context.hora_inicio,
        hora_fin=context.hora_fin,
        tipo_reserva=context.tipo_reserva,
        ciudadano=context.ciudadano)

    #assert context.reservado
    pass
##########################FIN PRIMER ESCENARIO####################################

@step('el ciudadano realice una reserva "privada" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, area_comunal, fecha_reserva, hora_inicio, hora_fin):
    context.tipo_reserva = "privada"
    context.fecha_reserva = fecha_reserva
    context.hora_inicio = hora_inicio
    context.hora_fin = hora_fin
    pass #da valor en el siguiente paso

@step('agregue los correos de los invitados "{correos_invitados}" a la reserva')
def step_impl(context, correos_invitados):
    context.controlador_reserva.obtener_reserva_por_id(id_reserva = context.id_reserva).agregar_correo_invitado(correos_invitados = correos_invitados)
    pass # esto puede ser verificado en el siguiente paso

#--------------------AQUI SE USA EL ENTONCES DE ARRIBA --------------------------#

@step("se enviará una invitación por correo con los detalles de la reserva.")
def step_impl(context):
    context.controlador_notificacion = ControladorNotificacion()
    #assert context.controlador_notificacion.enviar_invitacion(id_reserva = context.ciudadano.obtener_reserva_por_id(id_reserva = context.id_reserva))
    pass
    # Esta es una consideracion que me da deepsek para agilizar el tiempo que demora en enviarse un mensaje y arrojar algun codigo de OK
    # from unittest.mock import patch
    #
    # @step("se enviará una invitación por correo...")
    # def step_impl(context):
    #     with patch('app.models.ControladorNotificacion.enviar_invitacion') as mock:
    #         context.reserva.notificar_invitados()
    #         assert mock.called


##########################FIN SEGUNDO ESCENARIO####################################


@step(
    'que el ciudadano tiene una reserva "publica" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):
    context.ciudadano2 = Ciudadano.objects.create_user(
        correo_electronico=fake.email(),
        nombre_completo=fake.name(),
        numero_identificacion=str(fake.random_number(digits=10)),
        contrasena="secret122"
    )

    context.id_reserva, context.reservado = context.controlador_reserva.reservar_area_comunal(
        area_comunal=context.cancha3,
        fecha_reserva=fecha,
        hora_inicio=hora_inicio,
        hora_fin=hora_fin,
        tipo_reserva="publica",
        ciudadano=context.ciudadano2
    )
    #assert context.reservado #se verifica que tiene la reserva
    pass

@step("cancele la reserva")
def step_impl(context):
    pass

@step("la reserva será eliminada de la agenda pública.")
def step_impl(context):
    #assert context.controlador_reserva.cancelar_reserva(id_reserva=context.id_reserva, ciudadano=context.ciudadano2) #verificar que se calcelo con un TRUE
    pass
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