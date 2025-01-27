"""
Script para inicializar datos de prueba en la base de datos.
"""
import os
import django
from django.utils import timezone
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servicios_ciudadanos.settings')
django.setup()

from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models import EntidadMunicipal, EventoMunicipal

def crear_superusuario():
    """Crea un superusuario para pruebas"""
    try:
        # Verificar si el usuario ya existe
        if not Ciudadano.objects.filter(correo_electronico='admin@admin.com').exists():
            superuser = Ciudadano.objects.create_superuser(
                correo_electronico='admin@admin.com',
                password='admin123',
                nombre_completo='Administrador',
                numero_identificacion='1234567890'
            )
            print(f'Superusuario creado: {superuser.correo_electronico}')
        else:
            # Si el usuario existe, actualizar su contraseña
            superuser = Ciudadano.objects.get(correo_electronico='admin@admin.com')
            superuser.set_password('admin123')
            superuser.save()
            print('Contraseña del superusuario actualizada')
    except Exception as e:
        print(f'Error al crear superusuario: {e}')

def crear_entidad_municipal():
    """Crea una entidad municipal de prueba"""
    try:
        # Verificar si la entidad ya existe
        entidad, created = EntidadMunicipal.objects.get_or_create(
            nombre='Municipio de Ejemplo',
            defaults={
                'direccion': 'Calle Principal 123',
                'telefono': '(02) 123-4567',
                'correo_electronico': 'contacto@municipio.gob.ec'
            }
        )
        if created:
            print(f'Entidad municipal creada: {entidad.nombre}')
        else:
            print('La entidad municipal ya existe')
        return entidad
    except Exception as e:
        print(f'Error al crear entidad municipal: {e}')
        return None

def crear_eventos():
    """Crea eventos de prueba"""
    eventos = [
        {
            'nombre_evento': 'Feria Artesanal',
            'descripcion_evento': 'Gran exposición de artesanías locales',
            'fecha_realizacion': timezone.now() + timedelta(days=7),
            'lugar_evento': 'Plaza Central',
            'capacidad_maxima': 100,
            'estado_actual': EventoMunicipal.ESTADO_PROGRAMADO
        },
        {
            'nombre_evento': 'Festival Cultural',
            'descripcion_evento': 'Música, danza y gastronomía local',
            'fecha_realizacion': timezone.now() + timedelta(days=14),
            'lugar_evento': 'Parque Municipal',
            'capacidad_maxima': 200,
            'estado_actual': EventoMunicipal.ESTADO_PROGRAMADO
        }
    ]
    
    for evento_data in eventos:
        try:
            # Verificar si el evento ya existe
            evento, created = EventoMunicipal.objects.get_or_create(
                nombre_evento=evento_data['nombre_evento'],
                defaults=evento_data
            )
            if created:
                print(f'Evento creado: {evento.nombre_evento}')
            else:
                print(f'El evento {evento.nombre_evento} ya existe')
        except Exception as e:
            print(f'Error al crear evento: {e}')

def main():
    """Función principal que ejecuta todas las inicializaciones"""
    print('Iniciando creación de datos de prueba...')
    
    # Crear superusuario
    crear_superusuario()
    
    # Crear entidad municipal
    crear_entidad_municipal()
    
    # Crear eventos
    crear_eventos()
    
    print('Proceso de inicialización completado.')

if __name__ == '__main__':
    main()
