"""
init_test_data.py

Este script inicializa datos de prueba:
  - Crea (o recupera) una EntidadMunicipal de prueba
  - Crea dos EspaciosPublicos asociados a dicha entidad
  - Crea 4 EventoMunicipal con diferentes estados:
    * Uno programado (fecha futura)
    * Uno en curso (fecha actual)
    * Uno cancelado
    * Uno finalizado
    Todos con aforo de 2 personas
  - Crea 7 ciudadanos con correos simples (nombre@test.com)
"""

import os
import django
import datetime

# Configuración del entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servicios_ciudadanos.settings")
django.setup()

from django.utils import timezone
from django.db import transaction

# Importar modelos y enums
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models import EspacioPublico, EntidadMunicipal
from entidad_municipal_app.models.evento.enums import EstadoEvento
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia
from entidad_municipal_app.models.evento.enums import EstadoRegistro, EstadoAsistencia

def create_test_data():
    # 1. Crear o recuperar una EntidadMunicipal de prueba
    entidad_email = "entidad@test.com"
    entidad_defaults = {
        "nombre": "Entidad Municipal Test",
        "direccion": "Calle Falsa 123",
        "telefono": "123456789",
        "is_staff": True,
        "is_active": True,
    }
    entidad, creada = EntidadMunicipal.objects.get_or_create(
        correo_electronico=entidad_email,
        defaults=entidad_defaults
    )
    if creada:
        entidad.set_password("test123")
        entidad.save()
        print("EntidadMunicipal creada.")
    else:
        print("La EntidadMunicipal ya existe.")

    # 2. Crear dos EspaciosPublicos asociados a la entidad
    espacio1, _ = EspacioPublico.objects.get_or_create(
        nombre="Plaza Central",
        defaults={
            "direccion": "Avenida Principal 123",
            "descripcion": "Plaza principal para eventos públicos",
            "entidad_municipal": entidad,
            "estado_espacio_publico": "DISPONIBLE"
        }
    )
    print(f"EspacioPublico creado: {espacio1.nombre}")

    espacio2, _ = EspacioPublico.objects.get_or_create(
        nombre="Parque Municipal",
        defaults={
            "direccion": "Calle del Parque 456",
            "descripcion": "Parque municipal para eventos al aire libre",
            "entidad_municipal": entidad,
            "estado_espacio_publico": "DISPONIBLE"
        }
    )
    print(f"EspacioPublico creado: {espacio2.nombre}")

    # 3. Crear eventos en diferentes estados
    ahora = timezone.now()
    
    with transaction.atomic():
        # Evento programado (futuro, 7 días después)
        evento_programado = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Feria Artesanal",
            descripcion="Gran feria de artesanías locales",
            fecha=ahora + datetime.timedelta(days=7),
            lugar=espacio1.direccion,
            capacidad=2,
            entidad_municipal=entidad,
            espacio_publico=espacio1
        )
        # No necesitamos cambiar el estado, ya viene PROGRAMADO por defecto
        print(f"Evento PROGRAMADO creado: {evento_programado.nombre_evento} - Estado: {evento_programado.estado_actual}")

        # Evento en curso (actual)
        evento_curso = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Festival de Música",
            descripcion="Festival de música en vivo",
            fecha=ahora - datetime.timedelta(hours=1),  # Comenzó hace 1 hora
            lugar=espacio2.direccion,
            capacidad=2,
            entidad_municipal=entidad,
            espacio_publico=espacio2
        )
        evento_curso.estado_actual = EstadoEvento.EN_CURSO.value
        evento_curso.save()
        print(f"Evento EN CURSO creado: {evento_curso.nombre_evento} - Estado: {evento_curso.estado_actual}")

        # Evento cancelado (estaba programado para mañana pero se canceló)
        evento_cancelado = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Exposición de Arte",
            descripcion="Exposición de arte local",
            fecha=ahora + datetime.timedelta(days=1),
            lugar="Centro Cultural",
            capacidad=2,
            entidad_municipal=entidad,
            espacio_publico=None
        )
        evento_cancelado.estado_actual = EstadoEvento.CANCELADO.value
        evento_cancelado.save()
        print(f"Evento CANCELADO creado: {evento_cancelado.nombre_evento} - Estado: {evento_cancelado.estado_actual}")

        # Evento finalizado (ocurrió hace 2 días)
        evento_finalizado = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Taller de Pintura",
            descripcion="Taller de pintura para principiantes",
            fecha=ahora - datetime.timedelta(days=2),
            lugar="Casa de la Cultura",
            capacidad=2,
            entidad_municipal=entidad,
            espacio_publico=None
        )
        evento_finalizado.estado_actual = EstadoEvento.FINALIZADO.value
        evento_finalizado.save()
        print(f"Evento FINALIZADO creado: {evento_finalizado.nombre_evento} - Estado: {evento_finalizado.estado_actual}")

    # 4. Crear 7 ciudadanos con correos simples
    ciudadanos_data = [
        {"nombre": "Juan", "apellido": "Pérez", "id": "ID001", "correo": "juan@test.com"},
        {"nombre": "María", "apellido": "García", "id": "ID002", "correo": "maria@test.com"},
        {"nombre": "Pedro", "apellido": "López", "id": "ID003", "correo": "pedro@test.com"},
        {"nombre": "Ana", "apellido": "Martínez", "id": "ID004", "correo": "ana@test.com"},
        {"nombre": "Luis", "apellido": "Rodríguez", "id": "ID005", "correo": "luis@test.com"},
        {"nombre": "Carlos", "apellido": "Sánchez", "id": "ID006", "correo": "carlos@test.com"},
        {"nombre": "Diana", "apellido": "Torres", "id": "ID007", "correo": "diana@test.com"},
    ]

    ciudadanos = []
    for data in ciudadanos_data:
        ciudadano = Ciudadano.objects.create(
            correo_electronico=data["correo"],
            nombre_completo=f"{data['nombre']} {data['apellido']}",
            numero_identificacion=data["id"],
            esta_activo=True
        )
        ciudadano.set_password("password123")  # Establecer contraseña
        ciudadano.save()
        ciudadanos.append(ciudadano)
        print(f"Ciudadano creado: {ciudadano.nombre_completo} - {ciudadano.correo_electronico}")

    # 5. Inscribir a los dos últimos ciudadanos a los eventos EN_CURSO, CANCELADO y FINALIZADO
    carlos_diana = ciudadanos[-2:]

    # Inscribir en evento EN_CURSO
    for ciudadano in carlos_diana:
        registro = RegistroAsistencia.objects.create(
            ciudadano=ciudadano,
            evento=evento_curso,
            estado_registro=EstadoRegistro.INSCRITO.value,
            estado_asistencia=EstadoAsistencia.PENDIENTE.value
        )
        print(f"Ciudadano {ciudadano.nombre_completo} inscrito en evento {evento_curso.nombre_evento}")

    # Inscribir en evento CANCELADO
    for ciudadano in carlos_diana:
        registro = RegistroAsistencia.objects.create(
            ciudadano=ciudadano,
            evento=evento_cancelado,
            estado_registro=EstadoRegistro.CANCELADO.value,  # Como el evento está cancelado, el registro también
            estado_asistencia=EstadoAsistencia.NO_ASISTIO.value  # Al estar cancelado, no asistió
        )
        print(f"Ciudadano {ciudadano.nombre_completo} inscrito en evento {evento_cancelado.nombre_evento}")

    # Inscribir en evento FINALIZADO
    for ciudadano in carlos_diana:
        registro = RegistroAsistencia.objects.create(
            ciudadano=ciudadano,
            evento=evento_finalizado,
            estado_registro=EstadoRegistro.INSCRITO.value,
            estado_asistencia=EstadoAsistencia.ASISTIO.value  # Como ya finalizó, asumimos que asistieron
        )
        print(f"Ciudadano {ciudadano.nombre_completo} inscrito en evento {evento_finalizado.nombre_evento}")

    print("\nResumen de datos creados:")
    print("- 1 Entidad Municipal")
    print("- 2 Espacios Públicos")
    print("- 4 Eventos:")
    print("  * PROGRAMADO: Feria Artesanal (aforo: 2)")
    print("  * EN_CURSO: Festival de Música (aforo: 2)")
    print("  * CANCELADO: Exposición de Arte (aforo: 2)")
    print("  * FINALIZADO: Taller de Pintura (aforo: 2)")
    print("- 7 Ciudadanos")

if __name__ == "__main__":
    create_test_data()