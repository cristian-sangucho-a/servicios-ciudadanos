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
from entidad_municipal_app.models.espacio_publico import EspacioPublico  # Importar el modelo EspacioPublico

##crear espacios publicos de prueba
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

        # Crear espacios públicos de prueba (2 disponibles y 2 no disponibles)
    espacios_publicos_data = [
        {"nombre": "Estadio Municipal", "direccion": "Avenida Deportes 202",
         "estado_espacio_publico": EspacioPublico.ESTADO_DISPONIBLE,
         "estado_incidente_espacio": EspacioPublico.NO_AFECTADO,
         "descripcion": "Estadio principal para eventos deportivos"},
        {"nombre": "Parque Central", "direccion": "Calle Principal 456",
         "estado_espacio_publico": EspacioPublico.ESTADO_DISPONIBLE,
         "estado_incidente_espacio": EspacioPublico.NO_AFECTADO, "descripcion": "Un hermoso parque central"},
        {"nombre": "Plaza Mayor", "direccion": "Avenida Libertad 789",
         "estado_espacio_publico": EspacioPublico.ESTADO_DISPONIBLE,
         "estado_incidente_espacio": EspacioPublico.NO_AFECTADO, "descripcion": "Una plaza principal en el centro"},
        {"nombre": "Plaza Central", "direccion": "Avenida 24 Mayo",
         "estado_espacio_publico": EspacioPublico.ESTADO_DISPONIBLE,
         "estado_incidente_espacio": EspacioPublico.NO_AFECTADO, "descripcion": "Una plaza principal en el centro"},
        {"nombre": "Centro Cultural", "direccion": "Calle Cultura 101",
         "estado_espacio_publico": EspacioPublico.ESTADO_NO_DISPONIBLE,
         "estado_incidente_espacio": EspacioPublico.NO_AFECTADO, "descripcion": "Centro para actividades culturales"},
    ]

    espacios_publicos = []
    for data in espacios_publicos_data:
        espacio_publico, created = EspacioPublico.objects.get_or_create(
            nombre=data["nombre"],
            defaults={
                "entidad_municipal": entidad_municipal,
                "direccion": data["direccion"],
                "descripcion": data["descripcion"],
                "estado_espacio_publico": data["estado_espacio_publico"],
                "estado_incidente_espacio": data["estado_incidente_espacio"]
            }
        )
        if created:
            print(f"✓ Creado espacio público: {espacio_publico.nombre} ({espacio_publico.estado_espacio_publico})")
        else:
            print(f"El espacio público {espacio_publico.nombre} ya existe")
        espacios_publicos.append(espacio_publico)

    # ahorita son datos de prueba se van a borrar

    # Crear eventos de prueba y asignarles un espacio público y relacionarle con la entidad que se ha creado
    ahora = timezone.now()
    eventos_data = [
        {"nombre_evento": "Concierto en el Parque", "descripcion_evento": "Gran concierto al aire libre con múltiples artistas", "fecha_realizacion": ahora + timezone.timedelta(days=7), "capacidad_maxima": 100, "espacio_publico": espacios_publicos[0]},
    ]


    for data in eventos_data:
        # Verificar si el espacio público ya está ocupado
        if data["espacio_publico"].estado_espacio_publico == EspacioPublico.ESTADO_NO_DISPONIBLE:
            print(f"El espacio público {data['espacio_publico'].nombre} no está disponible para el evento {data['nombre_evento']}")
            continue

        # Crear el evento
        evento, created = EventoMunicipal.objects.get_or_create(
            nombre_evento=data["nombre_evento"],
            defaults={
                "descripcion_evento": data["descripcion_evento"],
                "fecha_realizacion": data["fecha_realizacion"],
                "capacidad_maxima": data["capacidad_maxima"],
                "estado_actual": EventoMunicipal.ESTADO_PROGRAMADO,
                "espacio_publico": data["espacio_publico"],  # Asignar el espacio público
                "entidad_municipal": entidad_municipal  # Asignar la entidad municipal
            }
        )
        if created:
            # Actualizar el estado del espacio público a NO DISPONIBLE
            data["espacio_publico"].estado_espacio_publico = EspacioPublico.ESTADO_NO_DISPONIBLE
            data["espacio_publico"].save()
            print(f"✓ Creado evento: {evento.nombre_evento} en {evento.espacio_publico.nombre}")
        else:
            print(f"El evento {evento.nombre_evento} ya existe")

    print('\n¡Datos de prueba creados exitosamente!')


def listar_datos():
    print("\n=== Entidades Municipales Registradas ===")
    entidades = EntidadMunicipal.objects.all()
    for entidad in entidades:
        print(f"\nEntidad: {entidad.nombre}")
        print(f"Correo: {entidad.correo_electronico}")
        print(f"Dirección: {entidad.direccion}")
        print(f"Teléfono: {entidad.telefono}")

        #ahorita son datos de prueba se van a borrar
        # Listar eventos de la entidad
        eventos = EventoMunicipal.objects.filter(entidad_municipal=entidad)
        if eventos.exists():
            print("\n  ── Eventos organizados ──")
            for evento in eventos:
                print(f"    - {evento.nombre_evento} ({evento.fecha_realizacion})")
                print(f"      Capacidad: {evento.capacidad_maxima}")
                print(f"      Estado: {evento.estado_actual}")
                print(f"      Ubicación: {evento.espacio_publico.nombre if evento.espacio_publico else 'No asignado'}")
        else:
            print("  No tiene eventos registrados.")

if __name__ == '__main__':
    crear_datos_prueba()
    listar_datos()

