from django.db import models
from entidad_municipal_app.models import EntidadMunicipal
class EspacioPublico(models.Model):
    """
    Modelo para representar un espacio público.
    """
    nombre = models.CharField(
        max_length=100,
        help_text="Nombre del espacio público",
        default="Espacio Público"
    )
    entidad_municipal = models.ForeignKey(
        EntidadMunicipal,
        on_delete=models.CASCADE,
        help_text="Entidad municipal a la que pertenece el espacio público",
        related_name = 'espacios_publicos'
    )
    direccion = models.CharField(
        max_length=200,
        help_text="Dirección del espacio público",
        default="Dirección no especificada"
    )
#--
    estado_incedente_espacio = models.CharField(
        max_length=20,
        choices=[("Afectado", "Afectado"), ("No Afectado", "No Afectado")],
        default="No Afectado",
        help_text="Estado del espacio público"
    )

    ESTADO_DISPONIBLE = 'DISPONIBLE'
    ESTADO_NO_DISPONIBLE = 'NO_DISPONIBLE'

    ESTADOS_DISPONIBILIDAD = [
        (ESTADO_DISPONIBLE, 'Disponible'),
        (ESTADO_NO_DISPONIBLE, 'No Disponible'),
    ]

    estado_espacioPublico = models.CharField(
        max_length=20,
        choices=ESTADOS_DISPONIBILIDAD,
        default=ESTADO_DISPONIBLE,
        help_text="Estado del espacio público en la fecha especificada"
    )

    @classmethod
    def obtener_por_nombre(cls, nombre):
        """
        Método para obtener un espacio público por su nombre.

        :param nombre: Nombre del espacio público a buscar.
        :return: Objeto EspacioPublico si se encuentra, None en caso contrario.
        """
        try:
            return cls.objects.get(nombre=nombre)
        except cls.DoesNotExist:
            return None



    def get_direccion(self):
        """
        Obtiene el lugar del evento.
        """
        return self.direccion

    def get_estado(self):
        """
        Método para obtener el estado del espacio público.
        """
        return dict(self.ESTADOS_DISPONIBILIDAD).get(self.estado_espacioPublico, 'Estado desconocido')

    def set_estado(self, nuevo_estado):
        """
        Método para cambiar el estado del espacio público.
        """
        if nuevo_estado in dict(self.ESTADOS_DISPONIBILIDAD):
            self.estado_espacioPublico = nuevo_estado
            self.save()  # Guarda el cambio en la base de datos
        else:
            raise ValueError(f"Estado no válido: {nuevo_estado}")

    def esta_disponible(self):
        """
        Método que verifica si el espacio público está disponible o no.
        """
        return self.estado_espacioPublico == EspacioPublico.ESTADO_DISPONIBLE

    def __str__(self):
        return f"{self.nombre} ({self.estado_incedente_espacio})"

    @property
    def estado_espacio_str(self):
        """
        Retorna el estado del espacio como una cadena de texto, sin modificar el campo original.
        """
        return self.get_estado_incedente_espacio_display()


    def __str__(self):
        return f"{self.nombre} - {'Disponible' if self.esta_disponible() else 'Ocupado'}"

    class Meta:
        verbose_name = "Espacio Público"
        verbose_name_plural = "Espacios Públicos"

