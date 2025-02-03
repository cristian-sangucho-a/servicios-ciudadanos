import django
import os
from django.utils import timezone

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicios_ciudadanos.settings')  # Reemplaza 'tu_proyecto' por el nombre de tu proyecto

# Inicializar Django
django.setup()

from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.EntidadMunicipal import EntidadMunicipal


def crear_datos_prueba():
    print('Iniciando creación de datos de prueba...')

    # Crear entidad municipal de prueba
    entidad_municipal, created = EntidadMunicipal.objects.get_or_create(
        correo_electronico="entidad@test.com",
        defaults={
            "nombre": "Entidad Municipal de Prueba",
            "direccion": "Calle Falsa 123",
            "telefono": "123456789"
        }
    )
    if created:
        entidad_municipal.set_password("test123")
        entidad_municipal.save()
        print(f"✓ Creada entidad municipal: {entidad_municipal.nombre}")
    else:
        print(f"La entidad municipal {entidad_municipal.nombre} ya existe")

    # Crear ciudadanos de prueba
    ciudadanos_data = [
        {"correo_electronico": "juan@test.com", "nombre_completo": "Juan Pérez", "numero_identificacion": "1234567890", "password": "test123"},
        {"correo_electronico": "maria@test.com", "nombre_completo": "María García", "numero_identificacion": "2345678901", "password": "test123"},
        {"correo_electronico": "pedro@test.com", "nombre_completo": "Pedro López", "numero_identificacion": "3456789012", "password": "test123"},
        {"correo_electronico": "ana@test.com", "nombre_completo": "Ana Martínez", "numero_identificacion": "4567890123", "password": "test123"},
        {"correo_electronico": "luis@test.com", "nombre_completo": "Luis Rodríguez", "numero_identificacion": "5678901234", "password": "test123"},
    ]

    for data in ciudadanos_data:
        ciudadano, created = Ciudadano.objects.get_or_create(
            correo_electronico=data["correo_electronico"],
            defaults={
                "nombre_completo": data["nombre_completo"],
                "numero_identificacion": data["numero_identificacion"]
            }
        )
        if created:
            # Usar el método set_password para cifrar la contraseña
            ciudadano.set_password(data["password"])
            ciudadano.save()
            print(f"✓ Creado ciudadano: {ciudadano.nombre_completo}")
        else:
            print(f"El ciudadano {ciudadano.nombre_completo} ya existe")

    # Crear eventos de prueba
    ahora = timezone.now()
    eventos_data = [
        {"nombre_evento": "Concierto en el Parque", "descripcion_evento": "Gran concierto al aire libre con múltiples artistas", "fecha_realizacion": ahora + timezone.timedelta(days=7), "capacidad_maxima": 100, "espacio_publico": espacios_publicos[0]},
        {"nombre_evento": "Taller de Arte", "descripcion_evento": "Taller exclusivo de pintura", "fecha_realizacion": ahora + timezone.timedelta(days=5), "capacidad_maxima": 1, "espacio_publico": espacios_publicos[1]},
        {"nombre_evento": "Feria Gastronómica","descripcion_evento": "Degustación de platos típicos de la región. Más de 30 expositores presentarán sus mejores creaciones culinarias.","fecha_realizacion": ahora + timezone.timedelta(days=3), "lugar_evento": "Plaza Mayor", "capacidad_maxima": 1,"espacio_publico": espacios_publicos[2]},
    ]

    for data in eventos_data:
        evento, created = EventoMunicipal.objects.get_or_create(
            nombre_evento=data["nombre_evento"],
            defaults={
                "descripcion_evento": data["descripcion_evento"],
                "fecha_realizacion": data["fecha_realizacion"],
                "lugar_evento": data["lugar_evento"],
                "capacidad_maxima": data["capacidad_maxima"],
                "estado_actual": EventoMunicipal.ESTADO_PROGRAMADO,
                "entidad_municipal": entidad_municipal  # Asociar a la entidad municipal
            }
        )
        if created:
            print(f"✓ Creado evento: {evento.nombre_evento}")
        else:
            print(f"El evento {evento.nombre_evento} ya existe")

    print('\n¡Datos de prueba creados exitosamente!')


if __name__ == '__main__':
    crear_datos_prueba()
