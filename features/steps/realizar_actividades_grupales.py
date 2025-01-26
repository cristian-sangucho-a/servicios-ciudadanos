from behave import *

#use_step_matcher("re")


@step('que existen areas comunales en el espacio publico "{nombre_espacio_publico}" disponibles en la ciudad y son')
def step_impl(context, nombre_espacio_publico):
    context.ciudad = Ciudad("Quito")
    context.espacio_publico = EspacioPublico(nombre_espacio_publico)
    context.cancha1 = AreaComunal(context.table[0].cells[0])
    context.cancha2 = AreaComunal(context.table[1].cells[0])
    context.cancha3 = AreaComunal(context.table[2].cells[0])

    context.espacio_publico.agregar_area_comunal(context.cancha1)
    context.espacio_publico.agregar_area_comunal(context.cancha2)
    context.espacio_publico.agregar_area_comunal(context.cancha3)

    context.cancha1.agregar_fecha_disponible("2021-06-01", "12:00", "18:00")
    context.cancha2.agregar_fecha_disponible("2021-06-01", "12:00", "18:00")
    context.cancha3.agregar_fecha_disponible("2021-06-01", "12:00", "18:00")

    assert context.ciudad.espacio_publico.hay_areas_comunales_disponibles();

@step('el ciudadano no supera las "{maximo_reservas}" reservas activas')
def step_impl(context, maximo_reservas):
    context.ciudadano = Ciudadano("Fernando Do Santos", "1725548763")
    assert context.ciudadano.obtener_numero_reservas_activas() <= maximo_reservas


@step('el ciudadano realice una reserva "publica" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, area_comunal, fecha_reserva, hora_inicio, hora_fin):
    context.tipo_reserva = "publica"
    context.fecha_reserva = fecha_reserva
    context.hora_inicio = hora_inicio
    context.hora_fin = hora_fin
    pass #da valor en el siguiente paso

@step('el ciudadano realice una reserva "privada" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, area_comunal, fecha_reserva, hora_inicio, hora_fin):
    context.tipo_reserva = "privada"
    context.fecha_reserva = fecha_reserva
    context.hora_inicio = hora_inicio
    context.hora_fin = hora_fin
    pass #da valor en el siguiente paso


@step("se guarda la reserva en la Agenda Pública.")
def step_impl(context):
    context.controlador_reserva = ControladorReserva()
    context.id_reserva, context.reservado = context.controlador_reserva.reservar_area_comunal(context.cancha1, context.fecha_reserva, context.hora_inicio, context.hora_fin, context.tipo_reserva, context.ciudadano)

    assert context.reservado

@step('agregue los correos de los invitados "{correos_invitados}" a la reserva')
def step_impl(context, correos_invitados):
    context.reserva.agregar_correo_invitado(correos_invitados)
    # context.correos_invitados = correos_invitados
    pass # esto puede ser verificado en el siguiente paso

@step("se enviará una invitación por correo con los detalles de la reserva.")
def step_impl(context):
    context.controlador_notificacion = ControladorNotificacion()
    assert context.controlador_notificacion.enviar_invitacion(context.ciudadano.obtener_reserva_por_id(context.id_reserva))


@step(
    'que el ciudadano tiene una reserva "{tipo_reserva}" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, tipo_reserva, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):
    context.id_reserva, context.reservado = context.controlador_reserva.reservar_area_comunal(
        context.cancha3,
        fecha,
        hora_inicio,
        hora_fin,
        tipo_reserva.lower(),  # Ej: "publica" → "publica"
        context.ciudadano  # Asume que context.ciudadano ya existe
    )


@step("cancele la reserva")
def step_impl(context):
    pass

@step("la reserva será eliminada de la agenda pública.")
def step_impl(context):
    assert context.controlador_reserva.cancelar_reserva(context.id_reserva, context.ciudadano)


@step("se enviará una correo de cancelacion de cancelación a los invitados")
def step_impl(context):
    assert context.controlador_notificacion.enviar_invitacion(
        context.ciudadano.obtener_reserva_por_id(context.id_reserva))
