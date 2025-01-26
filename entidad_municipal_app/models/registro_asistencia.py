"""
Modelo que gestiona los registros de asistencia a eventos municipales.
"""
from django.db import models
from django.core.exceptions import ValidationError
from ciudadano_app.models import Ciudadano

class RegistroAsistenciaManager(models.Manager):
    """Manager personalizado para consultas comunes de RegistroAsistencia"""
    
    def inscritos_para_ciudadano(self, ciudadano):
        """Obtiene todos los registros activos de un ciudadano"""
        return self.filter(
            ciudadano=ciudadano,
            estado_registro=RegistroAsistencia.ESTADO_INSCRITO
        )
    
    def en_espera_para_ciudadano(self, ciudadano):
        """Obtiene todos los registros en lista de espera de un ciudadano"""
        return self.filter(
            ciudadano=ciudadano,
            estado_registro=RegistroAsistencia.ESTADO_EN_ESPERA
        )
    
    def obtener_siguiente_en_espera(self, evento):
        """Obtiene el siguiente registro en lista de espera para un evento"""
        return self.filter(
            evento=evento,
            estado_registro=RegistroAsistencia.ESTADO_EN_ESPERA
        ).order_by('fecha_inscripcion').first()

    def tiene_inscripcion_activa(self, evento, ciudadano):
        """Verifica si un ciudadano tiene una inscripción activa en un evento"""
        return self.filter(
            evento=evento,
            ciudadano=ciudadano,
            estado_registro__in=[
                RegistroAsistencia.ESTADO_INSCRITO,
                RegistroAsistencia.ESTADO_EN_ESPERA
            ]
        ).exists()

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
        'entidad_municipal_app.EventoMunicipal',  # Referencia lazy para evitar importación circular
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
    
    fecha_modificacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Modificación',
        help_text='Fecha y hora de la última modificación'
    )

    objects = RegistroAsistenciaManager()

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
