"""
Repositorio en memoria para eventos municipales.
Contiene métodos para crear datos de prueba para varios modelos.
"""

from faker import Faker
from django.utils import timezone

from datetime import datetime, timedelta

from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.enums import EstadoEvento, EstadoEspacioPublico

fake = Faker('es_ES')

def crear_ciudadano_aleatorio():
    """Crea un ciudadano con datos aleatorios"""
    return Ciudadano.objects.create(
        correo_electronico=fake.email(),
        nombre_completo=f"{fake.first_name()} {fake.last_name()}",
        numero_identificacion=str(fake.random_number(digits=10, fix_len=True))
    )
    
def crear_entidad_municipal_aleatoria():
    """Crea una entidad municipal con datos aleatorios"""
    return EntidadMunicipal.objects.create(
        nombre=fake.company(),
        direccion=fake.address(),
        telefono=fake.phone_number(),
        correo_electronico=fake.email(),
        fecha_registro=datetime.now()
    )
    
def crear_espacio_publico_aleatorio(nombre_espacio="", estado="", entidad_municipal=None):
    """Crea un espacio público con datos aleatorios o específicos"""
    if not nombre_espacio:
        nombre_espacio = fake.company()
    
    if not estado:
        estado = EstadoEspacioPublico.DISPONIBLE.value
    
    if not entidad_municipal:
        entidad_municipal = crear_entidad_municipal_aleatoria()

    return EspacioPublico.objects.create(
        nombre=nombre_espacio,
        entidad_municipal=entidad_municipal,
        estado_espacio_publico=estado,
    )

def crear_evento_aleatorio(capacidad=10):
    """Crea un evento con datos aleatorios y capacidad específica"""
    entidad = crear_entidad_municipal_aleatoria()
    espacio = crear_espacio_publico_aleatorio(
        "Parque Central", 
        EstadoEspacioPublico.DISPONIBLE.value,
        entidad
    )

    return EventoMunicipal.objects.crear_evento_con_aforo(
        nombre="Concierto de Música",
        descripcion="Un concierto al aire libre con artistas locales.",
        fecha=timezone.now() + timedelta(days=7),
        lugar="Parque Central",
        capacidad=capacidad,
        entidad_municipal=entidad,
        espacio_publico=espacio,
    )
