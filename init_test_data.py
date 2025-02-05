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

# Importar modelos
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models import EspacioPublico, EntidadMunicipal
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

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
    espacio1 = EspacioPublico.objects.create(
        nombre="Plaza Central",
        direccion="Avenida Siempre Viva 742",
        descripcion="Espacio público para eventos en el centro de la ciudad.",
        entidad_municipal=entidad,
        estado_espacio_publico="DISPONIBLE"  # Asegurarse de que el estado coincida con el definido en el enum
    )
    print(f"EspacioPublico creado: {espacio1.nombre}")

    # Espacio para el segundo evento
    espacio2 = EspacioPublico.objects.create(
        nombre="Parque Central",
        direccion="Calle del Parque 456",
        descripcion="Parque ideal para actividades al aire libre.",
        entidad_municipal=entidad,
        estado_espacio_publico="DISPONIBLE"
    )
    print(f"EspacioPublico creado: {espacio2.nombre}")

    # 3. Crear dos EventoMunicipal usando el método 'crear_evento_con_aforo'
    # Primer evento: Festival de Primavera
    fecha_evento1 = timezone.now() + datetime.timedelta(days=1)
    evento1 = EventoMunicipal.objects.crear_evento_con_aforo(
        nombre="Festival de Primavera",
        descripcion="Evento para celebrar la llegada de la primavera con música y actividades al aire libre.",
        fecha=fecha_evento1,
        lugar=espacio1.direccion,  # Se reemplaza por la dirección del espacio público
        capacidad=100,
        entidad_municipal=entidad,
        espacio_publico=espacio1
    )
    print(f"EventoMunicipal creado: {evento1.nombre_evento}")

    # Segundo evento: Feria de Verano
    fecha_evento2 = timezone.now() + datetime.timedelta(days=3)
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
    
    print("Se han creado 5 ciudadanos disponibles para inscripción (sin inscribirlos a los eventos).")

if __name__ == "__main__":
    create_test_data()
