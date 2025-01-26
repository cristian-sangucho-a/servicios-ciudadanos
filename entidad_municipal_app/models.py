from django.db import models
from django.core.exceptions import ValidationError
from ciudadano_app.models import Ciudadano

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
    
    cupos_disponibles = models.PositiveIntegerField(
        verbose_name='Cupos Disponibles',
        help_text='Número de cupos aún disponibles'
    )
    
    estado_actual = models.CharField(
        max_length=20,
        choices=ESTADOS_EVENTO,
        default=ESTADO_PROGRAMADO,
        verbose_name='Estado',
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

    class Meta:
        verbose_name = 'Evento Municipal'
        verbose_name_plural = 'Eventos Municipales'
        ordering = ['-fecha_realizacion']

    def verificar_disponibilidad_cupos(self):
        """Verifica si hay cupos disponibles para el evento"""
        return self.cupos_disponibles > 0

    def verificar_estado_permite_inscripciones(self):
        """Verifica si el evento está en un estado que permite inscripciones"""
        return self.estado_actual == self.ESTADO_PROGRAMADO

    def reducir_cupo_disponible(self):
        """Reduce en uno el número de cupos disponibles"""
        if not self.verificar_disponibilidad_cupos():
            raise ValidationError("No hay cupos disponibles para este evento")
        self.cupos_disponibles -= 1
        self.save()

    def aumentar_cupo_disponible(self):
        """Aumenta en uno el número de cupos disponibles"""
        if self.cupos_disponibles < self.capacidad_maxima:
            self.cupos_disponibles += 1
            self.save()

    def obtener_formato_fecha(self):
        """Retorna la fecha del evento en formato legible"""
        return self.fecha_realizacion.strftime('%d/%m/%Y %H:%M')

    def __str__(self):
        return f"{self.nombre_evento} ({self.obtener_formato_fecha()})"


class RegistroAsistencia(models.Model):
    """
    Modelo que gestiona las inscripciones de ciudadanos a eventos municipales.
    Maneja estados de inscripción y lista de espera.
    """
    
    ESTADO_INSCRITO = 'INSCRITO'
    ESTADO_EN_ESPERA = 'EN_ESPERA'
    ESTADO_CANCELADO = 'CANCELADO'
    ESTADO_ASISTIO = 'ASISTIO'
    ESTADO_NO_ASISTIO = 'NO_ASISTIO'
    
    ESTADOS_REGISTRO = [
        (ESTADO_INSCRITO, 'Inscrito'),
        (ESTADO_EN_ESPERA, 'En Lista de Espera'),
        (ESTADO_CANCELADO, 'Cancelado'),
        (ESTADO_ASISTIO, 'Asistió'),
        (ESTADO_NO_ASISTIO, 'No Asistió'),
    ]

    ciudadano = models.ForeignKey(
        Ciudadano,
        on_delete=models.CASCADE,
        verbose_name='Ciudadano',
        help_text='Ciudadano que se inscribe al evento'
    )
    
    evento = models.ForeignKey(
        EventoMunicipal,
        on_delete=models.CASCADE,
        verbose_name='Evento',
        help_text='Evento al que se inscribe el ciudadano'
    )
    
    estado_registro = models.CharField(
        max_length=20,
        choices=ESTADOS_REGISTRO,
        verbose_name='Estado del Registro',
        help_text='Estado actual de la inscripción'
    )
    
    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Inscripción',
        help_text='Fecha y hora en que se realizó la inscripción'
    )
    
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Actualización',
        help_text='Fecha y hora de la última modificación'
    )

    class Meta:
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencia'
        unique_together = ['ciudadano', 'evento']
        ordering = ['fecha_inscripcion']

    def verificar_estado_activo(self):
        """Verifica si la inscripción está en un estado activo"""
        return self.estado_registro in [self.ESTADO_INSCRITO, self.ESTADO_EN_ESPERA]

    def actualizar_estado(self, nuevo_estado):
        """
        Actualiza el estado del registro de asistencia
        
        Args:
            nuevo_estado: Nuevo estado a establecer
            
        Raises:
            ValidationError: Si el estado no es válido
        """
        if nuevo_estado not in dict(self.ESTADOS_REGISTRO):
            raise ValidationError(f"Estado no válido: {nuevo_estado}")
        self.estado_registro = nuevo_estado
        self.save()

    def obtener_formato_fecha_inscripcion(self):
        """Retorna la fecha de inscripción en formato legible"""
        return self.fecha_inscripcion.strftime('%d/%m/%Y %H:%M')

    def __str__(self):
        return f"{self.ciudadano.obtener_nombre_completo()} - {self.evento.nombre_evento} ({self.estado_registro})"
