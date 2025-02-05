#!/usr/bin/env python
"""
init_test_data.py

Este script inicializa datos de prueba:
  - Crea (o recupera) una EntidadMunicipal de prueba.
  - Crea dos EspaciosPublicos asociados a dicha entidad.
  - Crea dos EventoMunicipal, cada uno asignado a un EspacioPublico.
  - Crea 5 ciudadanos disponibles para inscribirse (sin inscribirlos en los eventos).

Para ejecutarlo:
    python init_test_data.py
"""

import os
import django
import datetime

# Configuración del entorno de Django. Ajusta "tu_proyecto.settings" según corresponda.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servicios_ciudadanos.settings")
django.setup()

from django.utils import timezone

# Importar modelos y enums
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models import EspacioPublico, EntidadMunicipal
from entidad_municipal_app.models.evento.enums import EstadoEspacioPublico
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

def print_espacio_info(espacio, titulo="Estado del Espacio"):
    """Imprime información detallada del espacio público"""
    print(f"\n{titulo}:")
    print("-" * 50)
    print(f"Nombre: {espacio.nombre}")
    print(f"Dirección: {espacio.direccion}")
    print(f"Estado actual: {espacio.estado_espacio_publico}")
    print(f"Estado esperado: {EstadoEspacioPublico.DISPONIBLE.value}")
    print(f"Estado incidente: {espacio.estado_incidente_espacio}")
    print(f"Estado incidente esperado: {EspacioPublico.NO_AFECTADO}")
    print(f"¿Estados correctos?: {espacio.estado_espacio_publico == EstadoEspacioPublico.DISPONIBLE.value and espacio.estado_incidente_espacio == EspacioPublico.NO_AFECTADO}")
    print("-" * 50)

def create_test_data():
    # 1. Crear o recuperar una EntidadMunicipal de prueba
    entidad_email = "entidadtest@example.com"
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
        entidad.set_password("testpassword")
        entidad.save()
        print("EntidadMunicipal creada.")
    else:
        print("La EntidadMunicipal ya existe.")

    # 2. Crear dos EspaciosPublicos asociados a la entidad
    # Espacio para el primer evento 
    espacio1, creado1 = EspacioPublico.objects.get_or_create(
        nombre="Plaza Central",
        defaults={
            "direccion": "Avenida Siempre Viva 742",
            "descripcion": "Espacio público para eventos en el centro de la ciudad.",
            "entidad_municipal": entidad,
            "estado_espacio_publico": EstadoEspacioPublico.DISPONIBLE.value,
            "estado_incidente_espacio": EspacioPublico.NO_AFECTADO
        }
    )
    
    if creado1:
        print(f"EspacioPublico creado: {espacio1.nombre}")
    else:
        print(f"EspacioPublico existente actualizado: {espacio1.nombre}")
        espacio1.estado_espacio_publico = EstadoEspacioPublico.DISPONIBLE.value
        espacio1.estado_incidente_espacio = EspacioPublico.NO_AFECTADO
        espacio1.save()
    
    print_espacio_info(espacio1, "Estado del Primer Espacio")

    # Espacio para el segundo evento
    espacio2, creado2 = EspacioPublico.objects.get_or_create(
        nombre="Parque Central",
        defaults={
            "direccion": "Calle del Parque 456",
            "descripcion": "Parque ideal para actividades al aire libre.",
            "entidad_municipal": entidad,
            "estado_espacio_publico": EstadoEspacioPublico.DISPONIBLE.value,
            "estado_incidente_espacio": EspacioPublico.NO_AFECTADO
        }
    )
    if creado2:
        print(f"EspacioPublico creado: {espacio2.nombre}")
    else:
        print(f"EspacioPublico existente actualizado: {espacio2.nombre}")
        espacio2.estado_espacio_publico = EstadoEspacioPublico.DISPONIBLE.value
        espacio2.estado_incidente_espacio = EspacioPublico.NO_AFECTADO
        espacio2.save()
    
    print_espacio_info(espacio2, "Estado del Segundo Espacio")

    # Crear 5 espacios públicos adicionales
    espacios_adicionales = [
        {
            "nombre": "Coliseo Municipal",
            "direccion": "Av. Deportiva 789",
            "descripcion": "Espacio cubierto para eventos deportivos y culturales.",
        },
        {
            "nombre": "Jardín Botánico",
            "direccion": "Calle de las Flores 234",
            "descripcion": "Hermoso jardín con diversas especies de plantas y áreas verdes.",
        },
        {
            "nombre": "Teatro Municipal",
            "direccion": "Av. de las Artes 567",
            "descripcion": "Teatro histórico para presentaciones artísticas y culturales.",
        },
        {
            "nombre": "Centro Comunitario",
            "direccion": "Calle Vecinal 890",
            "descripcion": "Espacio multiusos para actividades comunitarias.",
        },
        {
            "nombre": "Mirador Ciudad",
            "direccion": "Av. de la Montaña 123",
            "descripcion": "Espacio al aire libre con vista panorámica de la ciudad.",
        }
    ]

    for espacio_data in espacios_adicionales:
        espacio, creado = EspacioPublico.objects.get_or_create(
            nombre=espacio_data["nombre"],
            defaults={
                "direccion": espacio_data["direccion"],
                "descripcion": espacio_data["descripcion"],
                "entidad_municipal": entidad,
                "estado_espacio_publico": EstadoEspacioPublico.DISPONIBLE.value,
                "estado_incidente_espacio": EspacioPublico.NO_AFECTADO
            }
        )
        if creado:
            print(f"EspacioPublico adicional creado: {espacio.nombre}")
        else:
            print(f"EspacioPublico adicional existente actualizado: {espacio.nombre}")
            espacio.estado_espacio_publico = EstadoEspacioPublico.DISPONIBLE.value
            espacio.estado_incidente_espacio = EspacioPublico.NO_AFECTADO
            espacio.save()
        print_espacio_info(espacio, f"Estado de {espacio.nombre}")

    # Verificar todos los espacios en la base de datos
    print("\nEstado de todos los espacios en la base de datos:")
    for espacio in EspacioPublico.objects.all():
        print_espacio_info(espacio, f"Estado de {espacio.nombre}")

    # 3. Crear dos EventoMunicipal usando el método 'crear_evento_con_aforo'
    # Primer evento: Festival de Primavera
    fecha_evento1 = timezone.localtime() + datetime.timedelta(days=1)
    evento1 = EventoMunicipal.objects.crear_evento_con_aforo(
        nombre="Festival de Primavera",
        descripcion="Evento para celebrar la llegada de la primavera con música y actividades al aire libre.",
        fecha=fecha_evento1,
        lugar=espacio1.direccion,
        capacidad=100,
        entidad_municipal=entidad,
        espacio_publico=espacio1
    )
    print(f"EventoMunicipal creado: {evento1.nombre_evento}")

    # Segundo evento: Feria de Verano
    fecha_evento2 = timezone.localtime() + datetime.timedelta(days=3)
    evento2 = EventoMunicipal.objects.crear_evento_con_aforo(
        nombre="Feria de Verano",
        descripcion="Gran feria con juegos, comida y actividades para toda la familia.",
        fecha=fecha_evento2,
        lugar=espacio2.direccion,
        capacidad=150,
        entidad_municipal=entidad,
        espacio_publico=espacio2
    )
    print(f"EventoMunicipal creado: {evento2.nombre_evento}")

    # 4. Crear 5 ciudadanos (sin inscribirlos a ningún evento)
    ciudadanos = []
    for i in range(1, 6):
        email = f"ciudadano{i}@example.com"
        nombre_completo = f"Ciudadano {i}"
        numero_identificacion = f"ID{i:03d}"  # Ejemplo: ID001, ID002, etc.
        
        ciudadano, creado = Ciudadano.objects.get_or_create(
            correo_electronico=email,
            defaults={
                "nombre_completo": nombre_completo,
                "numero_identificacion": numero_identificacion,
            }
        )
        if creado:
            ciudadano.set_password("password123")
            ciudadano.save()
            print(f"Ciudadano creado: {ciudadano.nombre_completo}")
        else:
            print(f"El ciudadano ya existe: {ciudadano.nombre_completo}")
        ciudadanos.append(ciudadano)
    
    print("\nResumen de la creación de datos de prueba:")
    print("------------------------------------------")
    print(f"- EntidadMunicipal: {entidad.nombre}")
    print(f"- Espacios Públicos: {espacio1.nombre} y {espacio2.nombre}")
    print(f"- Eventos: {evento1.nombre_evento} y {evento2.nombre_evento}")
    print("- 5 ciudadanos creados y disponibles para inscripción")
    print("\nPuedes iniciar sesión como:")
    print(f"Entidad Municipal - Email: {entidad_email}, Password: testpassword")
    print("Ciudadanos - Email: ciudadanoX@example.com (donde X va de 1 a 5), Password: password123")

if __name__ == "__main__":
    create_test_data()
