from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico, EventoMunicipal
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models.evento.enums import EstadoEspacioPublico, EstadoEvento

class Command(BaseCommand):
    help = 'Inicializa datos de prueba para el sistema de eventos municipales'

    def handle(self, *args, **kwargs):
        self.stdout.write('Creando datos de prueba...')

        # Limpiar datos existentes
        EntidadMunicipal.objects.all().delete()
        Ciudadano.objects.all().delete()
        EspacioPublico.objects.all().delete()
        EventoMunicipal.objects.all().delete()

        # 1. Crear Entidad Municipal
        entidad = EntidadMunicipal.objects.create_user(
            correo_electronico='municipio@test.com',
            password='testpass123',
            nombre='Municipio de Prueba',
            direccion='Calle Principal 123',
            telefono='0987654321'
        )
        self.stdout.write(self.style.SUCCESS(f'Entidad Municipal creada: {entidad.nombre}'))

        # 2. Crear Espacios Públicos
        espacio1 = EspacioPublico.objects.create(
            nombre='Plaza Central',
            direccion='Av. Principal 100',
            descripcion='Plaza principal del municipio',
            entidad_municipal=entidad,
            estado_espacio_publico=EstadoEspacioPublico.DISPONIBLE.value
        )

        espacio2 = EspacioPublico.objects.create(
            nombre='Coliseo Municipal',
            direccion='Calle Deportes 200',
            descripcion='Coliseo techado para eventos',
            entidad_municipal=entidad,
            estado_espacio_publico=EstadoEspacioPublico.DISPONIBLE.value
        )
        self.stdout.write(self.style.SUCCESS('Espacios públicos creados'))

        # 3. Crear Ciudadanos
        ciudadanos = []
        for i in range(5):
            ciudadano = Ciudadano.objects.create_user(
                correo_electronico=f'ciudadano{i+1}@test.com',
                password='testpass123',
                nombre_completo=f'Ciudadano Prueba {i+1}',
                numero_identificacion=f'1750000000{i+1}'
            )
            ciudadanos.append(ciudadano)
        self.stdout.write(self.style.SUCCESS('Ciudadanos creados'))

        # 4. Crear Eventos
        # Evento con cupos disponibles
        fecha_futura1 = timezone.now() + timedelta(days=7)
        evento1 = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Festival Cultural",
            descripcion="Gran festival cultural con artistas locales",
            fecha=fecha_futura1,
            lugar="Plaza Central",
            capacidad=50,
            entidad_municipal=entidad,
            espacio_publico=espacio1
        )

        # Evento con cupos limitados (para probar lista de espera)
        fecha_futura2 = timezone.now() + timedelta(days=14)
        evento2 = EventoMunicipal.objects.crear_evento_con_aforo(
            nombre="Concierto Municipal",
            descripcion="Concierto con la orquesta sinfónica",
            fecha=fecha_futura2,
            lugar="Coliseo Municipal",
            capacidad=3,  # Capacidad pequeña para probar lista de espera
            entidad_municipal=entidad,
            espacio_publico=espacio2
        )
        self.stdout.write(self.style.SUCCESS('Eventos creados'))

        # 5. Inscribir algunos ciudadanos en los eventos
        # Inscripciones en evento1 (quedarán cupos disponibles)
        evento1.inscribir_ciudadano(ciudadanos[0])
        evento1.inscribir_ciudadano(ciudadanos[1])
        
        # Inscripciones en evento2 (se llenará y tendrá lista de espera)
        evento2.inscribir_ciudadano(ciudadanos[0])  # INSCRITO
        evento2.inscribir_ciudadano(ciudadanos[1])  # INSCRITO
        evento2.inscribir_ciudadano(ciudadanos[2])  # INSCRITO
        evento2.inscribir_ciudadano(ciudadanos[3])  # EN_ESPERA
        evento2.inscribir_ciudadano(ciudadanos[4])  # EN_ESPERA

        self.stdout.write(self.style.SUCCESS('Datos de prueba creados exitosamente'))
