"""
Modelo que representa un evento municipal.
"""
from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Count
from django.db import transaction
from django.db.models import F, Q
from django.utils import timezone
from .registro_asistencia import RegistroAsistencia

from entidad_municipal_app.models import EntidadMunicipal
from entidad_municipal_app.models import espacio_publico


class EventoMunicipal(models.Model):
    """
    Modelo que representa un evento organizado por la entidad municipal.
    Gestiona el aforo y estado del evento.
    """
    
    ESTADO_PROGRAMADO = 'PROGRAMADO'
    ESTADO_EN_CURSO = 'EN_CURSO'
    ESTADO_FINALIZADO = 'FINALIZADO'
    ESTADO_CANCELADO = 'CANCELADO'
    
    ESTADOS_EVENTO = [
        (ESTADO_PROGRAMADO, 'Programado'),
        (ESTADO_EN_CURSO, 'En Curso'),
        (ESTADO_FINALIZADO, 'Finalizado'),
        (ESTADO_CANCELADO, 'Cancelado'),
    ]

    # Estados de registro (copiados de RegistroAsistencia para evitar importación circular)
    ESTADO_INSCRITO = 'INSCRITO'
    ESTADO_EN_ESPERA = 'EN_ESPERA'
    ESTADO_CANCELADO_REGISTRO = 'CANCELADO'
    ESTADO_ASISTIO = 'ASISTIO'
    ESTADO_NO_ASISTIO = 'NO_ASISTIO'

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
    """
    lugar_evento = models.CharField(
        max_length=200,
        verbose_name='Lugar',
        help_text='Ubicación donde se realizará el evento'
    )
    """
    capacidad_maxima = models.PositiveIntegerField(
        verbose_name='Capacidad Máxima',
        help_text='Número máximo de personas que pueden asistir'
    )
    
    estado_actual = models.CharField(
        max_length=20,
        choices=ESTADOS_EVENTO,
        default=ESTADO_PROGRAMADO,
        verbose_name='Estado del Evento',
        help_text='Estado actual del evento'
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
#---


    lugar_evento = models.ForeignKey(
        'EspacioPublico',
        on_delete=models.CASCADE,
        null=True,  # Permite valores nulos
        blank=True,  # Permite valores vacíos en formularios
        verbose_name='Lugar',
        help_text='Espacio público donde se realizará el evento'
    )

    #fecha y hora de inicio y fin

    class Meta:
        verbose_name = 'Evento Municipal'
        verbose_name_plural = 'Eventos Municipales'
        ordering = ['-fecha_realizacion']
##--
    @property
    def estado_espacio(self):
        """
        Verifica el estado del espacio asociado al evento.
        """
        if self.lugar_evento:
            return self.lugar_evento.estado_espacio
        return None

    @property
    def cupos_disponibles(self):
        """
        Calcula los cupos disponibles del evento de forma atómica
        """
        return self.capacidad_maxima - self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_INSCRITO
        ).count()

    def _get_cupos_ocupados(self):
        """Obtiene el número de cupos ocupados"""
        return self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_INSCRITO
        ).count()

    def reducir_cupo_disponible(self):
        """
        Reduce el cupo disponible de forma segura con manejo de concurrencia
        
        Returns:
            bool: True si se pudo reducir el cupo, False si no hay cupos disponibles
        """
        with transaction.atomic():
            # Bloquea el registro para operaciones concurrentes
            evento = EventoMunicipal.objects.select_for_update().get(pk=self.pk)
            if evento.cupos_disponibles > 0:
                return True
            return False

    def aumentar_cupo_disponible(self):
        """
        Aumenta el cupo disponible de forma segura con manejo de concurrencia
        
        Returns:
            bool: True si se pudo aumentar el cupo, False si no se pudo aumentar
        """
        with transaction.atomic():
            # Bloquea el registro para operaciones concurrentes
            evento = EventoMunicipal.objects.select_for_update().get(pk=self.pk)
            if evento.capacidad_maxima > evento._get_cupos_ocupados():
                return True
            return False

    def esta_disponible_para_inscripcion(self):
        """
        Verifica si el evento está disponible para inscripciones
        
        Returns:
            bool: True si el evento está disponible para inscripciones
        """
        return (
            self.estado_actual == self.ESTADO_PROGRAMADO and
            self.fecha_realizacion > timezone.now() and
            self.cupos_disponibles > 0
        )

    def obtener_inscritos(self):
        """
        Obtiene la lista de ciudadanos inscritos al evento
        
        Returns:
            QuerySet: QuerySet de RegistroAsistencia con estado INSCRITO
        """
        return self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_INSCRITO
        ).select_related('ciudadano')

    def obtener_lista_espera(self):
        """
        Obtiene la lista de espera ordenada por fecha de inscripción
        
        Returns:
            QuerySet: QuerySet de RegistroAsistencia con estado EN_ESPERA
        """
        return self.registroasistencia_set.filter(
            estado_registro=self.ESTADO_EN_ESPERA
        ).select_related('ciudadano').order_by('fecha_inscripcion')

    def obtener_formato_fecha(self):
        """Retorna la fecha del evento en formato legible"""
        return self.fecha_realizacion.strftime("%d/%m/%Y %H:%M")

    def get_lugar_evento(self):
        """
        Obtiene el lugar del evento.
        """
        return self.lugar_evento

    def set_lugar_evento(self, lugar):
        """
        Establece el lugar del evento.

        Args:
            lugar (str): La nueva ubicación del evento.
        """
        self.lugar_evento = lugar
        self.save()


    def __str__(self):
        return f"{self.nombre_evento} ({self.obtener_formato_fecha()})"
