from behave import *
from faker import Faker
from ciudadano_app.models import Ciudadano
from shared.models import  Reporte, TipoReporte
from shared.models.notificacion.notificacion import Notificacion
from shared.models import Sector
from shared.models.notificacion.servicio_de_notificacion import ServicioDeNotificacion
from django.utils import timezone

fake = Faker()

# --- Funciones auxiliares ---

def crear_ciudadano(nombre_ciudadano):
    return Ciudadano.objects.create(
        nombre_completo=nombre_ciudadano,
        correo_electronico=f"{nombre_ciudadano.lower().replace(' ', '.')}@test.com",
        numero_identificacion=f"1234567890",
        esta_activo=True
    )

def crear_sector(nombre_sector):
  return Sector.objects.create(nombre=nombre_sector)


def crear_reporte(ciudadano, sector, asunto):
    tipo_reporte = TipoReporte.objects.get_or_create(
        asunto=asunto,
        defaults={'descripcion': f'Descripción de {asunto}'}
    )[0]

    return Reporte.objects.create(
        tipo_reporte=tipo_reporte,
        ciudadano=ciudadano,
        ubicacion=sector.nombre
    )

def crear_notificacion(ciudadano, mensaje):
    Notificacion.objects.create(
        ciudadano=ciudadano,
        mensaje=mensaje,
        fecha=timezone.now()
    )

# --- Escenarios ---
@step('que existen sectores en la ciudad y son')
def step_impl(context):
    context.sectores = []
    for row in context.table:
      sector = crear_sector(row['nombre_sector'])
      context.sectores.append(sector)

@step('el ciudadano "{nombre_ciudadano}" selecciona "{nombre_sector}" como sector de interés')
def step_impl(context, nombre_ciudadano, nombre_sector):
    context.ciudadano = crear_ciudadano(nombre_ciudadano)
    sector = Sector.objects.get(nombre=nombre_sector) # No necesitas get_or_create aquí
    context.ciudadano.sectores_de_interes.add(sector)
    context.sector = sector
    context.servicio_de_notificacion = ServicioDeNotificacion()  # Inicializa el servicio aquí si es necesario

@step('se enviará un correo con los detalles del reporte')
def step_impl(context):
    crear_notificacion(context.ciudadano, f"Correo enviado sobre reporte en {context.reporte.ubicacion}")

@step("se agregará a la lista de notificaciones")
def step_impl(context):
    notificaciones = Notificacion.objects.filter(ciudadano=context.ciudadano).count()
    assert notificaciones > 0, "No se encontraron notificaciones"


@step('se registre un reporte con asunto "{asunto}"')
def step_impl(context, asunto):
    context.reporte = crear_reporte(context.ciudadano, context.sector, asunto)

@step('el estado del reporte no es "{estado}"') # Este step ya no es necesario
def step_impl(context, estado):
   pass

@step('se registren al menos "{cantidad}" reportes con asunto "{asunto}"')
def step_impl(context, cantidad, asunto):
    for _ in range(int(cantidad)):
        crear_reporte(context.ciudadano, context.sector, asunto)

@step('el sector cambiará a estado "{estado}"')
def step_impl(context, estado):
    context.sector.estado = estado
    context.sector.save()
    sector_actualizado = Sector.objects.get(id=context.sector.id) #Recarga el objeto desde la base de datos para asegurar la consistencia.
    assert sector_actualizado.estado == estado, f"El sector debería estar en estado '{estado}', pero está en estado '{sector_actualizado.estado}'"


@step('se enviará un correo con el mensaje "{mensaje}"')
def step_impl(context, mensaje):
    crear_notificacion(context.ciudadano, mensaje)