from behave import step
from faker import Faker
from datetime import datetime
from ciudadano_app.models.area_comunal import AreaComunal
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.reserva.servicio_reserva import ServicioReserva
from ciudadano_app.models.servicio_notificacion_correo import ServicioNotificacionPorCorreo
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico

fake = Faker()
servicio_reserva = ServicioReserva()
servicio_notificacion_por_correo = ServicioNotificacionPorCorreo()

@step('que existen areas comunales disponibles en el espacio publico "{nombre_espacio_publico}" en la ciudad y son')
def step_impl(context, nombre_espacio_publico):
    """
    Crea un contexto donde se configuran áreas comunales disponibles en un espacio público.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.
        nombre_espacio_publico (str): El nombre del espacio público donde se encuentran las áreas comunales.

    Steps:
        - Se crea una entidad municipal mock.
        - Se configura un espacio público asociado a la entidad municipal.
        - Se agregan áreas comunales al espacio público desde la tabla de datos del contexto.
        - Se verifica que haya áreas comunales disponibles en el espacio público.

    Raises:
        AssertionError: Si no hay áreas comunales disponibles.
    """
    context.entidad_municipal = EntidadMunicipal.objects.create(
        nombre="Municipalidad Mock",
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email(),
        fecha_registro=datetime.now()
    )
    context.espacio_publico = EspacioPublico.objects.create(
        nombre=nombre_espacio_publico,
        entidad_municipal=context.entidad_municipal
    )
    for row in context.table:
        context.area_comunal = AreaComunal.objects.create(
            nombre_area=row['Nombre'],
            hora_de_apertura=datetime.strptime("08:00", "%H:%M").time(),
            hora_de_cierre=datetime.strptime("20:00", "%H:%M").time(),
            espacio_publico=context.espacio_publico
        )

    assert servicio_reserva.hay_areas_comunales_disponibles(context.espacio_publico)


@step('el ciudadano no supera las "{maximo_reservas}" reservas activas')
def step_impl(context, maximo_reservas):
    """
    Verifica que un ciudadano no supere el número máximo de reservas activas.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.
        maximo_reservas (str): El número máximo de reservas activas permitidas.

    Steps:
        - Se crea un ciudadano mock.
        - Se verifica que el ciudadano no supere el límite de reservas activas.

    Raises:
        AssertionError: Si el ciudadano supera el número máximo de reservas activas.
    """
    context.ciudadano = Ciudadano.objects.create(
        nombre_completo=fake.name(),
        correo_electronico=fake.email(),
        numero_identificacion=str(fake.random_number(digits=10))
    )
    context.maximo_reservas = int(maximo_reservas)
    assert not servicio_reserva.ciudadano_supera_maximo_reservas(ciudadano=context.ciudadano)


@step('el ciudadano realice una reserva de tipo "{tipo_reserva}" en el area comunal "{area_comunal}" el "{fecha_reserva}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, tipo_reserva, area_comunal, fecha_reserva, hora_inicio, hora_fin):
    """
    Simula la realización de una reserva por parte de un ciudadano.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.
        tipo_reserva (str): El tipo de reserva ("pública" o "privada").
        area_comunal (str): El nombre del área comunal donde se realiza la reserva.
        fecha_reserva (str): La fecha de la reserva en formato YYYY-MM-DD.
        hora_inicio (str): La hora de inicio de la reserva en formato HH:MM.
        hora_fin (str): La hora de fin de la reserva en formato HH:MM.

    Steps:
        - Se configuran los detalles de la reserva en el contexto.
    """
    context.tipo_reserva = tipo_reserva
    context.fecha_reserva = fecha_reserva
    context.hora_inicio = hora_inicio
    context.hora_fin = hora_fin
    context.correos_invitados = None


@step("se guarda la reserva en la Agenda Pública")
def step_impl(context):
    """
    Guarda la reserva en la agenda pública y verifica que se haya realizado correctamente.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.

    Steps:
        - Se reserva el área comunal en la agenda pública.
        - Si hay correos de invitados, se agregan a la reserva.
        - Se verifica que la reserva se haya realizado correctamente.

    Raises:
        AssertionError: Si la reserva no se pudo realizar.
    """
    fecha_formateada = datetime.strptime(context.fecha_reserva, "%d/%m/%Y").date()
    hora_inicio_formateada = datetime.strptime(context.hora_inicio, "%H:%M").time()
    hora_fin_formateada = datetime.strptime(context.hora_fin, "%H:%M").time()

    area_comunal = servicio_reserva.obtener_area_comunal(1)

    context.id_reserva, reservado = servicio_reserva.reservar_area_comunal(
        area_comunal=area_comunal, fecha_reserva=fecha_formateada,
        hora_inicio=hora_inicio_formateada, hora_fin=hora_fin_formateada, tipo_reserva=context.tipo_reserva,
        ciudadano=context.ciudadano, correos_invitados="")
    assert reservado


@step('agregue los correos de los invitados "{correos_invitados}" a la reserva')
def step_impl(context, correos_invitados):
    """
    Agrega correos de invitados a una reserva existente.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.
        correos_invitados (str): Los correos electrónicos de los invitados separados por comas.

    Steps:
        - Se actualiza el contexto con los correos de los invitados.
    """
    context.correos_invitados = correos_invitados


@step("se enviará una invitación por correo con los detalles de la reserva.")
def step_impl(context):
    """
    Verifica que se envíe una invitación por correo con los detalles de la reserva.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.

    Steps:
        - Se verifica que el servicio de reserva envíe correctamente la invitación.

    Raises:
        AssertionError: Si no se pudo enviar la invitación.
    """

    assert servicio_notificacion_por_correo.enviar_invitacion(servicio_reserva.obtener_reserva_por_id(context.id_reserva))



@step('que el ciudadano tiene una reserva de tipo "{tipo_reserva}" en el espacio publico "{nombre_espacio}" en el area comunal "{nombre_area}" el "{fecha}" de "{hora_inicio}" a "{hora_fin}"')
def step_impl(context, tipo_reserva, nombre_espacio, nombre_area, fecha, hora_inicio, hora_fin):
    """
    Configura un contexto donde un ciudadano tiene una reserva en un espacio público.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.
        tipo_reserva (str): El tipo de reserva ("pública" o "privada").
        nombre_espacio (str): El nombre del espacio público.
        nombre_area (str): El nombre del área comunal.
        fecha (str): La fecha de la reserva en formato YYYY-MM-DD.
        hora_inicio (str): La hora de inicio de la reserva en formato HH:MM.
        hora_fin (str): La hora de fin de la reserva en formato HH:MM.

    Steps:
        - Se crea un contexto para la reserva.
        - Se reserva el área comunal en la agenda pública.
        - Si es una reserva privada, se agregan correos de invitados.
        - Se verifica que la reserva se haya realizado correctamente.

    Raises:
        AssertionError: Si la reserva no se pudo realizar.
    """
    area_comunal = crear_contexto_para_la_reserva(context, nombre_espacio, nombre_area)
    fecha_formateada = datetime.strptime(fecha, "%d/%m/%Y").date()
    hora_inicio_formateada = datetime.strptime(hora_inicio, "%H:%M").time()
    hora_fin_formateada = datetime.strptime(hora_fin, "%H:%M").time()

    if tipo_reserva == "privado":
        correos_invitados = fake.email() + "," + fake.email()
    else:
        correos_invitados = ""

    context.id_reserva, reservado = servicio_reserva.reservar_area_comunal(
        fecha_reserva=fecha_formateada, hora_inicio=hora_inicio_formateada, hora_fin=hora_fin_formateada, tipo_reserva=tipo_reserva,
        area_comunal=area_comunal, ciudadano=context.ciudadano, correos_invitados=correos_invitados)
    assert reservado


@step("cancele la reserva")
def step_impl(context):
    """
    Simula la cancelación de una reserva por parte del ciudadano.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.

    Steps:
        - Este paso está vacío y se completa en el siguiente paso.
    """
    pass  # Da valor en el siguiente paso


@step("la reserva será eliminada de la agenda pública.")
def step_impl(context):
    """
    Verifica que la reserva se elimine correctamente de la agenda pública.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.

    Steps:
        - Se cancela la reserva utilizando el servicio de reserva.
        - Se verifica que la cancelación se haya realizado correctamente.

    Raises:
        AssertionError: Si la reserva no se pudo cancelar.
    """
    assert servicio_reserva.cancelar_reserva(id_reserva=context.id_reserva,
                                                        ciudadano=context.ciudadano)  # verificar que se calcelo con un TRUE


@step("se enviará una correo de cancelacion a los invitados")
def step_impl(context):
    """
    Verifica que se envíe un correo de cancelación a los invitados de la reserva.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.

    Steps:
        - Se verifica que el servicio de reserva envíe correctamente el correo de cancelación.

    Raises:
        AssertionError: Si no se pudo enviar el correo de cancelación.
    """
    assert servicio_notificacion_por_correo.enviar_cancelacion(servicio_reserva.obtener_reserva_por_id(context.id_reserva))


def crear_contexto_para_la_reserva(context, nombre_espacio, nombre_area):
    """
    Crea un contexto básico para configurar una reserva.

    Args:
        context (behave.runner.Context): El contexto del escenario de prueba.
        nombre_espacio (str): El nombre del espacio público.

    Steps:
        - Se crea una entidad municipal mock.
        - Se configura un espacio público asociado a la entidad municipal.
        - Se agregan áreas comunales al espacio público.
        - Se crea un ciudadano mock.
    """
    context.entidad_municipal = EntidadMunicipal.objects.create(
        nombre="Municipalidad Mock",
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email(),
        fecha_registro=datetime.now()
    )
    context.espacio_publico = EspacioPublico.objects.create(
        nombre=nombre_espacio,
        entidad_municipal=context.entidad_municipal
    )
    area_comunal = AreaComunal.objects.create(
        nombre_area=nombre_area,
        hora_de_apertura=datetime.strptime("08:00", "%H:%M").time(),
        hora_de_cierre=datetime.strptime("20:00", "%H:%M").time(),
        espacio_publico=context.espacio_publico
    )
    context.ciudadano = Ciudadano.objects.create(
        nombre_completo=fake.name(),
        correo_electronico=fake.email(),
        numero_identificacion=str(fake.random_number(digits=10)),
        esta_activo=True
    )
    return area_comunal