"""
Modelo que representa el registro de asistencia a un evento municipal.
"""
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from .enums import EstadoRegistro
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

class RegistroAsistencia(models.Model):
    """
    Modelo que registra la asistencia de un ciudadano a un evento municipal.
    """
    ciudadano = models.ForeignKey(
        Ciudadano,
        on_delete=models.CASCADE,
        related_name='registros',
        verbose_name='Ciudadano',
        help_text='Ciudadano que se registra al evento'
    )
    evento = models.ForeignKey(
        'entidad_municipal_app.EventoMunicipal',
        on_delete=models.CASCADE,
        related_name='registroasistencia_set',  # Nombre explícito para el set relacionado
        verbose_name='Evento',
        help_text='Evento al que se registra el ciudadano'
    )
    estado_registro = models.CharField(
        max_length=20,
        choices=EstadoRegistro.choices(),
        default=EstadoRegistro.INSCRITO.value,
        verbose_name='Estado del registro',
        help_text='Estado actual del registro de asistencia'
    )
    fecha_inscripcion = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de inscripción',
        help_text='Fecha y hora en que se realizó el registro'
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name='Última actualización',
        help_text='Fecha y hora de la última modificación'
    )

    class Meta:
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencia'
        ordering = ['-fecha_inscripcion']
        indexes = [
            models.Index(fields=['estado_registro']),
            models.Index(fields=['fecha_inscripcion']),
        ]
        unique_together = ['ciudadano', 'evento']

    @property
    def esta_activo(self):
        """Indica si el registro está en un estado activo (inscrito o en espera)."""
        return self.estado_registro in [
            EstadoRegistro.INSCRITO.value,
            EstadoRegistro.EN_ESPERA.value
        ]

    @property
    def esta_cancelado(self):
        """Indica si el registro está cancelado."""
        return self.estado_registro == EstadoRegistro.CANCELADO.value

    def cancelar(self):
        """Cancela el registro de asistencia."""
        self.estado_registro = EstadoRegistro.CANCELADO.value
        self.save()

    def reactivar(self, cupos_disponibles):
        """
        Reactiva un registro cancelado.
        El estado se determina según los cupos disponibles.
        """
        self.estado_registro = EstadoRegistro.determinar_estado(cupos_disponibles)
        self.save()

    def promover_a_inscrito(self):
        """Promueve un registro de EN_ESPERA a INSCRITO."""
        if self.estado_registro != EstadoRegistro.EN_ESPERA.value:
            raise ValueError("Solo se pueden promover registros en estado EN_ESPERA")
        self.estado_registro = EstadoRegistro.INSCRITO.value
        self.save()

    def actualizar_estado(self, nuevo_estado):
        """
        Actualiza el estado del registro validando las transiciones permitidas.
        
        Args:
            nuevo_estado: Nuevo estado a asignar (debe ser un valor de EstadoRegistro)
            
        Raises:
            ValidationError: Si el estado no es válido o la transición no está permitida
        """
        if nuevo_estado not in [e.value for e in EstadoRegistro]:
            raise ValidationError(f"Estado no válido: {nuevo_estado}")
        
        # Definir transiciones permitidas
        transiciones_validas = {
            EstadoRegistro.INSCRITO.value: [EstadoRegistro.EN_ESPERA.value, EstadoRegistro.CANCELADO.value],
            EstadoRegistro.EN_ESPERA.value: [EstadoRegistro.INSCRITO.value, EstadoRegistro.CANCELADO.value],
            EstadoRegistro.CANCELADO.value: [],  # No se permite cambiar desde cancelado
            EstadoRegistro.ASISTIO.value: [],    # No se permite cambiar desde asistió
            EstadoRegistro.NO_ASISTIO.value: [], # No se permite cambiar desde no asistió
        }
        
        if nuevo_estado not in transiciones_validas.get(self.estado_registro, []):
            raise ValidationError(
                f"No se permite cambiar de {self.estado_registro} a {nuevo_estado}"
            )
        
        self.estado_registro = nuevo_estado
        self.save()

    def __str__(self):
        return f"Registro de {self.ciudadano} en {self.evento.nombre} ({self.estado_registro})"
