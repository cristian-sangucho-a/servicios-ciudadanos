# archivo: entidad_municipal_app/models/evento/evento_municipal.py

from django.db import models, transaction
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.conf import settings
from .registro_asistencia import RegistroAsistencia
from .excepciones import ErrorGestionEventos
from .enums import EstadoEvento, EstadoRegistro, EstadoEspacioPublico
from .notificaciones import GestorNotificaciones

class EventoMunicipalManager(models.Manager):
    @transaction.atomic
    def crear_evento_con_aforo(self, nombre, descripcion, fecha, lugar, capacidad, entidad_municipal, espacio_publico=None):
        """
        Crea un evento municipal controlado, asignando espacio público y gestionando el aforo.
        """
        if espacio_publico:
            if espacio_publico.estado_espacio_publico != EstadoEspacioPublico.DISPONIBLE.value:
                raise ValidationError("El espacio público no está disponible")
            lugar = espacio_publico.direccion
            espacio_publico.estado_espacio_publico = EstadoEspacioPublico.NO_DISPONIBLE.value
            espacio_publico.save()

        return self.create(
            nombre_evento=nombre,
            descripcion_evento=descripcion,
            fecha_realizacion=fecha,
            lugar_evento=lugar,
            capacidad_maxima=capacidad,
            estado_actual=EstadoEvento.PROGRAMADO.value,
            espacio_publico=espacio_publico,
            entidad_municipal=entidad_municipal
        )

class EventoMunicipal(models.Model):
    """
    Modelo que representa un evento organizado por la entidad municipal.
    Gestiona el aforo y el registro de asistencias.
    """
    # Campos (se conservan los nombres existentes para evitar migraciones)
    nombre_evento = models.CharField(
        max_length=200,
        verbose_name='Nombre del Evento',
        help_text='Nombre descriptivo del evento municipal'
    )
    descripcion_evento = models.TextField(
        verbose_name='Descripción',
        help_text='Descripción detallada del evento'
    )
    fecha_realizacion = models.DateTimeField(
        verbose_name='Fecha de Realización',
        help_text='Fecha y hora en que se realizará el evento'
    )
    lugar_evento = models.CharField(
        max_length=200,
        verbose_name='Lugar',
        help_text='Ubicación donde se realizará el evento'
    )
    capacidad_maxima = models.PositiveIntegerField(
        verbose_name='Capacidad Máxima',
        help_text='Número máximo de personas que pueden asistir'
    )
    estado_actual = models.CharField(
        max_length=20,
        choices=EstadoEvento.choices(),
        default=EstadoEvento.PROGRAMADO.value,
        verbose_name='Estado del Evento',
        help_text='Estado actual del evento'
    )
    motivo_cancelacion = models.TextField(
        max_length=200,
        blank=True,
        default="",
        verbose_name='Motivo de Cancelación',
        help_text='Razón por la que se canceló el evento'
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Creación',
        help_text='Fecha y hora en que se creó el registro del evento'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización',
        help_text='Fecha y hora de la última modificación'
    )
    # Relaciones
    espacio_publico = models.ForeignKey(
        'entidad_municipal_app.EspacioPublico',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='eventos',
        verbose_name='Espacio Público',
        help_text='Espacio público donde se realizará el evento'
    )
    entidad_municipal = models.ForeignKey(
        'entidad_municipal_app.EntidadMunicipal',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='entidad',
        verbose_name='Entidad Municipal',
        help_text='Entidad municipal que organiza el evento'
    )

    objects = EventoMunicipalManager()

    class Meta:
        verbose_name = 'Evento Municipal'
        verbose_name_plural = 'Eventos Municipales'
        ordering = ['-fecha_realizacion']
        indexes = [
            models.Index(fields=['estado_actual']),
            models.Index(fields=['fecha_realizacion']),
        ]

    # Propiedad calculada para cupos disponibles (se usa el set relacionado de RegistroAsistencia)
    @property
    def cupos_disponibles(self):
        """Retorna la cantidad de cupos disponibles (capacidad máxima menos la cantidad de registros con estado INSCRITO)."""
        return self.capacidad_maxima - self.registroasistencia_set.filter(
            estado_registro=EstadoRegistro.INSCRITO.value
        ).count()

    # Propiedad para obtener los registros activos (INSCRITO o EN_ESPERA)
    @property
    def registros_activos(self):
        """Retorna el QuerySet de registros en estado INSCRITO o EN_ESPERA."""
        return self.registroasistencia_set.filter(
            estado_registro__in=[EstadoRegistro.INSCRITO.value, EstadoRegistro.EN_ESPERA.value]
        )

    # Métodos de negocio
    @transaction.atomic
    def inscribir_ciudadano(self, ciudadano):
        """
        Gestiona la inscripción de un ciudadano al evento.
        Se determina el estado (INSCRITO o EN_ESPERA) en función de los cupos disponibles.
        Se envía notificación al ciudadano.
        """
        # Se bloquea el evento para evitar condiciones de carrera
        evento = EventoMunicipal.objects.select_for_update().get(pk=self.pk)
        try:
            registro_existente = evento.registroasistencia_set.get(ciudadano=ciudadano)
            return self._gestionar_registro_existente(registro_existente)
        except RegistroAsistencia.DoesNotExist:
            return self._crear_nuevo_registro(ciudadano)

    @transaction.atomic
    def cancelar_inscripcion(self, registro_id):
        """
        Cancela una inscripción y, en caso de ser necesario, promueve al siguiente en lista de espera.
        
        Se determina el estado (INSCRITO o EN_ESPERA) en función de los cupos disponibles.
        Se envía notificación al ciudadano.
        """
        try:
            registro = self.registroasistencia_set.select_for_update().get(pk=registro_id)
            if registro.evento_id != self.pk:
                raise ErrorGestionEventos("El registro no pertenece a este evento")
            if registro.estado_registro == EstadoRegistro.CANCELADO.value:
                raise ErrorGestionEventos("El registro ya está cancelado")
            
            estado_original = registro.estado_registro
            registro.cancelar()

            registro_promovido = None
            if estado_original == EstadoRegistro.INSCRITO.value:
                # (Aquí se podría liberar el cupo; en esta lógica se confía en que la consulta de cupos_disponibles se actualice)
                registro_promovido = self._promover_siguiente_en_espera()

            # Enviar notificaciones (la función interna se encarga de ello)
            self._enviar_notificacion_inscripcion(registro)
            if registro_promovido:
                self._enviar_notificacion_inscripcion(registro_promovido)
            return registro, registro_promovido

        except RegistroAsistencia.DoesNotExist:
            raise ErrorGestionEventos("Registro de asistencia no encontrado")

    # Métodos auxiliares (privados)
    def _crear_nuevo_registro(self, ciudadano):
        nuevo_estado = EstadoRegistro.determinar_estado(self.cupos_disponibles)
        registro = self.registroasistencia_set.create(
            ciudadano=ciudadano,
            estado_registro=nuevo_estado
        )
        self._enviar_notificacion_inscripcion(registro)
        return registro

    def _gestionar_registro_existente(self, registro):
        if registro.esta_activo:
            raise ErrorGestionEventos("Ya tienes una inscripción activa para este evento")
        if registro.esta_cancelado:
            registro.reactivar(self.cupos_disponibles)
            self._enviar_notificacion_inscripcion(registro)
        return registro

    def _promover_siguiente_en_espera(self):
        siguiente = self.obtener_lista_espera().first()
        if siguiente:
            siguiente.promover_a_inscrito()
            self._enviar_notificacion_inscripcion(siguiente)
            return siguiente
        return None

    def _enviar_notificacion_inscripcion(self, registro):
        """
        Delegamos el envío de notificaciones a un servicio dedicado.
        (Actualmente la notificación está camuflada; se podrá implementar luego)
        """
        GestorNotificaciones.enviar_notificacion_inscripcion(registro=registro, evento=self)

    def obtener_lista_espera(self):
        """
        Retorna un QuerySet con los registros que están en lista de espera,
        ordenados por fecha de inscripción (FIFO).
        """
        return self.registroasistencia_set.filter(
            estado_registro=EstadoRegistro.EN_ESPERA.value
        ).order_by('fecha_inscripcion')

    def obtener_todos_registros(self):
        """
        Retorna un QuerySet con todos los registros del evento.
        """
        return self.registroasistencia_set.all()

    def clean(self):
        if self.estado_actual == EstadoEvento.CANCELADO.value and not self.motivo_cancelacion:
            raise ValidationError("Debe proporcionar un motivo para cancelar el evento")

    def __str__(self):
        return f"{self.nombre_evento} ({self.fecha_realizacion.strftime('%d/%m/%Y %H:%M')})"
