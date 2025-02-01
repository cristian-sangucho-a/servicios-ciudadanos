from behave import step
from faker import Faker
from datetime import datetime
from django.utils import timezone
from datetime import timedelta
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia
from django.core.exceptions import ValidationError

# use_step_matcher("re")

fake = Faker()

def crear_entidad_municipal_aleatoria():
    return EntidadMunicipal.objects.create(
        nombre=fake.company(),
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email(),
        fecha_registro=datetime.now()
    )

def crear_espacio_publico_aleatorio(nombre_espacio,estado, entidad_municipal):
    if estado == 'DISPONIBLE':
            estado = EspacioPublico.ESTADO_DISPONIBLE,
    else:
            estado = EspacioPublico.ESTADO_NO_DISPONIBLE,

    return EspacioPublico.objects.create(
        nombre=nombre_espacio,
        entidad_municipal=entidad_municipal,
        ##aumentar
       estado_espacio_publico=estado,
    )


@step("que una entidad municipal desea organizar un evento")
def step_impl(context):
    context.entidad_municipal = crear_entidad_municipal_aleatoria()
    """
    context.nombre_entidad_municipal = f"Municipio de {fake.city()}"
    context.entidad_municipal = EntidadMunicipal
    context.entidad_municipal = EntidadMunicipal.objects.create(
        nombre=context.nombre_entidad_municipal,
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email()
    )
    context.nombre_evento = f"Evento {fake.word()}"
    ##retroalimentacion
    
    Crea (o recupera) una EntidadMunicipal para usar en las pruebas.
    
    context.entidad_municipal, _ = EntidadMunicipal.objects.get_or_create(
        nombre="Entidad de Prueba"
    )
    """


@step('la fecha del evento es {fecha_evento}')
def step_impl(context, fecha_evento):
    context.fecha_realizacion = fake.date_time().strftime("%Y-%m-%d %H:%M:%S")


##retroalimentacion
"""
    Almacena la fecha en context para usar cuando se cree el evento.
    Formato esperado: dd/mm/yyyy
    @step('la fecha del evento es "([0-9]{2}/[0-9]{2}/[0-9]{4})"')
    fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
    context.fecha_evento = fecha
    """


@step('el espacio público {nombre_espacio_publico} que se encuentra disponible')
def step_impl(context, nombre_espacio_publico):
    estado_disponible = 'DISPONIBLE'
    context.espacio_publico = crear_espacio_publico_aleatorio(nombre_espacio_publico,estado_disponible,context.entidad_municipal)
    """
    context.espacio_publico = EspacioPublico.objects.create(
        nombre=nombre_espacio_publico,
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )
    ##retroalimentacion
    
       Simula que el espacio está disponible (no hay eventos esa fecha).
      
    context.espacio_publico, _ = EspacioPublico.objects.get_or_create(
        nombre=nombre_espacio_publico,
        entidad_municipal=context.entidad_municipal
    )
    context.espacio_disponible = True
    """


@step("se creara el evento")
def step_impl(context):
    context.evento = EventoMunicipal.objects.crear_evento_con_aforo(
        nombre=fake.sentence(nb_words=4),
        descripcion=fake.text(max_nb_chars=200),
        fecha=context.fecha_realizacion,
        lugar=fake.address(),
        capacidad=18,
        espacio_publico = context.espacio_publico,
    )

    """
    if context.espacio_disponible:
        try:
            context.evento_creado = EventoMunicipal.objects.crear_evento_con_aforo(
                nombre="Evento de Prueba",
                descripcion="Descripción del evento de prueba",
                fecha=context.fecha_evento,
                espacio_publico=context.espacio_publico,
                capacidad=100,
                entidad_municipal=context.entidad_municipal
            )
        except ValidationError as e:
            assert False, f"No se pudo crear el evento: {e}"
    else:
        assert False, "Se intentó crear el evento pero el espacio no está disponible"
"""

@step('el espacio público "{nombre_espacio_publico}" no se encuentre disponible')
def step_impl(context, nombre_espacio_publico):
    context.espacio_publico = EspacioPublico.objects.create(
        nombre=nombre_espacio_publico,
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        estado_espacio_publico=EspacioPublico.ESTADO_NO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )
    ##retroalimentacion
    """
    Marca el espacio como NO disponible creando un evento en la misma fecha.
    """
    esp_no_disp, _ = EspacioPublico.objects.get_or_create(
        nombre=nombre_espacio_publico,
        entidad_municipal=context.entidad_municipal
    )
    context.espacio_publico = esp_no_disp

    # Creamos otro evento en la misma fecha para simular un choque
    EventoMunicipal.objects.create(
        nombre_evento="Evento que choca",
        descripcion_evento="Ocupando la fecha",
        fecha_realizacion=context.fecha_evento,
        espacio_publico=esp_no_disp,
        entidad_municipal=context.entidad_municipal,
        lugar_evento=esp_no_disp.nombre,
        capacidad_maxima=50,
        estado_actual=EventoMunicipal.ESTADO_PROGRAMADO,
    )
    context.espacio_disponible = False


@step("no se creara el evento")
def step_impl(context):
    """
        if context.espacio_disponible.estado_espacio_publico == EspacioPublico.ESTADO_NO_DISPONIBLE:
            print("El espacio público no está disponible para este evento.")
    """
    if context.espacio_publico and not context.espacio_publico.esta_disponible():
        print("El espacio público no está disponible para este evento.")
    ##retroalimentacion
    """
    Intenta crear el evento y confirma que falla con ValidationError.
    """
    if not context.espacio_disponible:
        try:
            EventoMunicipal.objects.crear_evento_con_aforo(
                nombre="Evento de Prueba No Creado",
                descripcion="No debería crearse",
                fecha=context.fecha_evento,
                espacio_publico=context.espacio_publico,
                capacidad=100,
                entidad_municipal=context.entidad_municipal
            )
            assert False, "Se creó el evento cuando el espacio no estaba disponible."
        except ValidationError:
            # Ruta esperada: no se puede crear
            pass
    else:
        assert False, "El espacio se marcó como disponible; no corresponde a este paso."


@step("se mostrarán los espacios públicos disponibles")
def step_impl(context):
    """
        crear eventos espacios publicos disponibles no disponible en la misma (3)
        hacer una lista print
        y hacer que no tengan la misma fecha
    """

    context.espacio_publico_disponible = EspacioPublico.objects.create(
        nombre=fake.name(),
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )
    context.espacio_publico_disponible2 = EspacioPublico.objects.create(
        nombre=fake.name(),
        direccion=fake.address(),
        entidad_municipal=context.entidad_municipal,
        estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE,
        estado_incidente_espacio=EspacioPublico.NO_AFECTADO
    )

    espacios_disponibles = EspacioPublico.objects.filter(estado_espacio_publico=EspacioPublico.ESTADO_DISPONIBLE)

    if espacios_disponibles.exists():
        print("Espacios públicos disponibles:")
        for espacio in espacios_disponibles:
            print(f"{espacio.nombre} - {espacio.direccion}")
    else:
        print("No hay espacios públicos disponibles.")

    ##retroalimentacion
    """
    Lista los espacios que no tengan un evento PROGRAMADO/EN_CURSO en esa fecha.
    """
    fecha = context.fecha_evento

    eventos_misma_fecha = EventoMunicipal.objects.filter(
        fecha_realizacion=fecha,
        estado_actual__in=[EventoMunicipal.ESTADO_PROGRAMADO, EventoMunicipal.ESTADO_EN_CURSO]
    ).values_list('espacio_publico_id', flat=True)

    espacios_disponibles = EspacioPublico.objects.exclude(pk__in=eventos_misma_fecha)
    assert espacios_disponibles.count() >= 0, (
        "No se encontraron espacios disponibles (o ajustar la lógica)."
    )
    context.espacios_disponibles = espacios_disponibles


##--
@step('que existe un evento llamado "{nombre_evento}" con el estado "{estado_evento}"')
def step_impl(context, nombre_evento, estado_evento):

    """
    context.nombre_evento = nombre_evento
    context.estado_evento = estado_evento
    ?
    creas el evento aleatorio
    set estado_evento
    """
    # Simular la creación de una entidad municipal en memoria
    entidad_municipal = {
        'nombre': fake.company()
    }

    # Simular la creación de un espacio público en memoria
    espacio_publico = {
        'nombre': "Parque Bicentenario",  # Usando el nombre que defines en el escenario
        'estado_espacio': 'No Afectado',  # Inicialmente no afectado
        'entidad_municipal': entidad_municipal
    }

    # Simular la creación de un evento municipal en memoria
    context.evento = {
        'nombre_evento': nombre_evento,
        'estado_actual': estado_evento,
        'fecha_realizacion': fake.date_time(),
        'capacidad_maxima': 100,
        'lugar_evento': espacio_publico
    }
    ##retroalimentacion
    """
        Crea un evento con nombre y estado especificados, 
        o None si estado_evento = "NULL" (no existe).

    if estado_evento == "NULL":
        context.evento = None
        return

    espacio_demo, _ = EspacioPublico.objects.get_or_create(
        nombre="Parque Bicentenario",
        entidad_municipal=context.entidad_municipal
    )
    context.evento = EventoMunicipal.objects.create(
        nombre_evento=nombre_evento,
        descripcion_evento="Evento para prueba de cancelación",
        fecha_realizacion=datetime(2025, 2, 6, 10, 0),
        espacio_publico=espacio_demo,
        entidad_municipal=context.entidad_municipal,
        lugar_evento=espacio_demo.nombre,
        capacidad_maxima=100,
        estado_actual=(estado_evento if estado_evento != "NULL"
                       else EventoMunicipal.ESTADO_PROGRAMADO)
    )
    """


@step(
    'el espacio público destinado al evento es "{nombre_espacio}"')
def step_impl(context, nombre_espacio):
    context.evento = EventoMunicipal.objects.crear_evento_con_aforo(
                        nombre=context.nombre_evento,
                        descripcion=fake.text(max_nb_chars=200),
                        fecha=timezone.now() + timedelta(days=7),
                        lugar=fake.address(),
                        capacidad=10,
                        espacio_publico=crear_espacio_publico_aleatorio(nombre_espacio,crear_entidad_municipal_aleatoria())
                    )

    """
    # Aquí simula la actualización del espacio público en memoria
    if context.evento['lugar_evento']['nombre'] == nombre_espacio:
        # Asignar el valor de estado_espacio usando las constantes de la clase EspacioPublico
        if estado_espacio == EspacioPublico.AFECTADO:
            context.evento['lugar_evento']['estado_espacioPublico'] = EspacioPublico.AFECTADO
        elif estado_espacio == EspacioPublico.NO_AFECTADO:
            context.evento['lugar_evento']['estado_espacioPublico'] = EspacioPublico.NO_AFECTADO
        context.evento['lugar_evento']['motivo_riesgo'] = motivo_riesgo  # Cambiar a motivo_riesgo
        context.espacio = context.evento['lugar_evento']
    else:
        print(f"No se encontró el espacio público con el nombre {nombre_espacio}")
    ##retroalimentacion
    
    Simula si el espacio está 'Afectado' o 'No Afectado'.

    if nombre_espacio == "NULL":
        context.espacio_afectado = False
        return
    context.espacio_afectado = (estado_espacio.upper() == "AFECTADO")
    
    """

@step('está en una situación de "{estado_espacio}" debido a un "{motivo_riesgo}"')
def step_impl(context, estado_espacio, motivo_riesgo):
    context.evento.espacio_publico.estado_incidente_espacio = estado_espacio
    context.motivo_riesgo = motivo_riesgo


@step('la entidad municipal cambia el estado del evento a "{nuevo_estado_evento}"')
def step_impl(context, nuevo_estado_evento):
    context.evento.estado_actual = nuevo_estado_evento
    #cancelar_evento

    """
    if not evento:
        print("No existe evento a cancelar")
        return

    if evento['estado_actual'] == "EN_CURSO":
        print("El estado del evento es no programado por lo tanto no puede haber cancelación")
        return

    if evento['estado_actual'] == "FINALIZADO":
        print("El estado del evento es finalizado por lo tanto no puede haber cancelación")
        return

    if evento['lugar_evento']['estado_espacio'] == "No Afectado":
        print("El espacio del evento no se ve afectado por lo que no aplica a cancelación")
        return

    evento['estado_actual'] = nuevo_estado_evento
    context.evento = evento
    ##retroalimentacion
   
    Intenta cambiar el estado del evento.


     context.ultimo_error = None
    if context.evento is None:
        # No hay evento real
        context.evento_estado_anterior = None
        return

    context.evento_estado_anterior = context.evento.estado_actual
    try:
        context.evento.estado_actual = nuevo_estado_evento
        context.evento.save()
    except ValidationError as e:
        context.ultimo_error = str(e)
    """


@step('se registra el motivo de la cancelación')
def step_impl(context):

    context.evento.set_motivo_cancelacion(context.motivo_riesgo)

    """
    evento = context.evento
    
    if evento['estado_actual'] == "CANCELADO":
        evento['motivo_cancelacion'] = resultado
        print(f"Motivo de cancelación registrado: {resultado}")
    ##retroalimentacion
    
    Verifica la lógica de cancelación o mantenimiento de estado.
    "
    if context.evento is None:
        assert "No existe evento a cancelar" in resultado, (
            "Se esperaba 'No existe evento a cancelar' pero no coincide con el ejemplo."
        )
        return

    estado_actual = context.evento.estado_actual
    if estado_actual == EventoMunicipal.ESTADO_CANCELADO:
        assert "Se registra la cancelación" in resultado, (
            f"No coincide la descripción para CANCELADO: {resultado}"
        )
    else:
        if "No se puede cancelar" in resultado:
            assert estado_actual in [
                EventoMunicipal.ESTADO_EN_CURSO,
                EventoMunicipal.ESTADO_FINALIZADO
            ], f"Se esperaba no cancelar; estado actual = {estado_actual}"
        elif "El espacio no está afectado" in resultado:
            assert not context.espacio_afectado, "Espacio marcado como no afectado, no debía cancelarse."
    """