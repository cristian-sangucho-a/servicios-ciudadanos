from django.core.management.base import BaseCommand
from django.utils import timezone
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from entidad_municipal_app.models.evento.evento_municipal import EventoMunicipal
from entidad_municipal_app.models.evento.registro_asistencia import RegistroAsistencia

class Command(BaseCommand):
    help = 'Crea datos de prueba para ciudadanos y eventos'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando creación de datos de prueba...')

        # Crear ciudadanos de prueba
        ciudadanos_data = [
            {
                "correo_electronico": "juan@test.com",
                "nombre_completo": "Juan Pérez",
                "numero_identificacion": "1234567890",
                "password": "test123"
            },
            {
                "correo_electronico": "maria@test.com",
                "nombre_completo": "María García",
                "numero_identificacion": "2345678901",
                "password": "test123"
            },
            {
                "correo_electronico": "pedro@test.com",
                "nombre_completo": "Pedro López",
                "numero_identificacion": "3456789012",
                "password": "test123"
            },
            {
                "correo_electronico": "ana@test.com",
                "nombre_completo": "Ana Martínez",
                "numero_identificacion": "4567890123",
                "password": "test123"
            },
            {
                "correo_electronico": "luis@test.com",
                "nombre_completo": "Luis Rodríguez",
                "numero_identificacion": "5678901234",
                "password": "test123"
            },
        ]

        ciudadanos = []
        for data in ciudadanos_data:
            try:
                ciudadano = Ciudadano.objects.get(
                    correo_electronico=data["correo_electronico"]
                )
                self.stdout.write(f"El ciudadano {ciudadano.nombre_completo} ya existe")
            except Ciudadano.DoesNotExist:
                try:
                    ciudadano = Ciudadano.objects.create_user(
                        correo_electronico=data["correo_electronico"],
                        password=data["password"],
                        nombre_completo=data["nombre_completo"],
                        numero_identificacion=data["numero_identificacion"]
                    )
                    self.stdout.write(self.style.SUCCESS(f"Creado ciudadano: {ciudadano.nombre_completo}"))
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error al crear ciudadano: {str(e)}"))
                    continue
            ciudadanos.append(ciudadano)

        # Crear eventos de prueba
        ahora = timezone.now()
        eventos_data = [
            {
                "nombre_evento": "Concierto en el Parque",
                "descripcion_evento": "Gran concierto al aire libre con múltiples artistas",
                "fecha_realizacion": ahora + timezone.timedelta(days=7),
                "lugar_evento": "Parque Central",
                "capacidad_maxima": 100,  # Evento con muchos cupos
            },
            {
                "nombre_evento": "Taller de Arte",
                "descripcion_evento": "Taller exclusivo de pintura",
                "fecha_realizacion": ahora + timezone.timedelta(days=5),
                "lugar_evento": "Centro Cultural",
                "capacidad_maxima": 1,  # Evento con 1 solo cupo
            },
            {
                "nombre_evento": "Feria Gastronómica",
                "descripcion_evento": "Degustación de platos típicos",
                "fecha_realizacion": ahora + timezone.timedelta(days=3),
                "lugar_evento": "Plaza Mayor",
                "capacidad_maxima": 2,  # Evento con 2 cupos
            }
        ]

        eventos = []
        for data in eventos_data:
            evento, created = EventoMunicipal.objects.get_or_create(
                nombre_evento=data["nombre_evento"],
                defaults={
                    "descripcion_evento": data["descripcion_evento"],
                    "fecha_realizacion": data["fecha_realizacion"],
                    "lugar_evento": data["lugar_evento"],
                    "capacidad_maxima": data["capacidad_maxima"],
                    "estado_actual": EventoMunicipal.ESTADO_PROGRAMADO
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Creado evento: {evento.nombre_evento}"))
            else:
                self.stdout.write(f"El evento {evento.nombre_evento} ya existe")
            eventos.append(evento)

        # Realizar inscripciones de prueba
        self.stdout.write("\nRealizando inscripciones de prueba...")

        # 1. Inscribir a Juan en el Taller de Arte (evento de 1 cupo)
        taller = eventos[1]  # Taller de Arte
        juan = ciudadanos[0]  # Juan
        try:
            registro = taller.inscribir_ciudadano(juan)
            self.stdout.write(self.style.SUCCESS(
                f"✓ {juan.nombre_completo} inscrito en {taller.nombre_evento}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al inscribir: {str(e)}"))

        # 2. Intentar inscribir a María en el Taller de Arte (debería ir a lista de espera)
        maria = ciudadanos[1]  # María
        try:
            registro = taller.inscribir_ciudadano(maria)
            self.stdout.write(self.style.SUCCESS(
                f"✓ {maria.nombre_completo} en lista de espera para {taller.nombre_evento}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al inscribir: {str(e)}"))

        # 3. Inscribir a Pedro y Ana en la Feria Gastronómica (2 cupos)
        feria = eventos[2]  # Feria Gastronómica
        pedro = ciudadanos[2]  # Pedro
        ana = ciudadanos[3]  # Ana
        
        for ciudadano in [pedro, ana]:
            try:
                registro = feria.inscribir_ciudadano(ciudadano)
                self.stdout.write(self.style.SUCCESS(
                    f"✓ {ciudadano.nombre_completo} inscrito en {feria.nombre_evento}"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error al inscribir: {str(e)}"))

        # 4. Intentar inscribir a Luis en la Feria (debería ir a lista de espera)
        luis = ciudadanos[4]  # Luis
        try:
            registro = feria.inscribir_ciudadano(luis)
            self.stdout.write(self.style.SUCCESS(
                f"✓ {luis.nombre_completo} en lista de espera para {feria.nombre_evento}"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al inscribir: {str(e)}"))

        # 5. Inscribir a todos en el Concierto (muchos cupos)
        concierto = eventos[0]  # Concierto
        for ciudadano in ciudadanos:
            try:
                registro = concierto.inscribir_ciudadano(ciudadano)
                self.stdout.write(self.style.SUCCESS(
                    f"✓ {ciudadano.nombre_completo} inscrito en {concierto.nombre_evento}"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error al inscribir: {str(e)}"))

        self.stdout.write(self.style.SUCCESS('\n¡Datos de prueba creados exitosamente!'))
