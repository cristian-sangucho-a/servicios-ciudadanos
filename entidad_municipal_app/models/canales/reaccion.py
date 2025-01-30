from django.db import models
from django.utils.timezone import now
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from .noticia import Noticia

class Reaccion(models.Model):
    """
    Reacciones de ciudadanos a noticias.

    Este modelo representa las reacciones que los ciudadanos pueden tener hacia una noticia publicada.
    Cada reacción es vinculada a una noticia y un ciudadano específico.

    Attributes:
        noticia (ForeignKey): La noticia a la cual se le está reaccionando.
        ciudadano (ForeignKey): El ciudadano que emite la reacción.
        tipo (str): El tipo de reacción. Puede ser 'me_gusta', 'interesante', 'no_me_gusta', 'gracioso', o 'triste'.
        fecha (datetime): La fecha y hora en que se registró la reacción. Se establece automáticamente a la fecha actual.
    """
    TIPOS_REACCION = [
        ('me_gusta', 'Me gusta'),
        ('interesante', 'Interesante'),
        ('no_me_gusta', 'No me gusta'),
        ('gracioso', 'Gracioso'),
        ('triste', 'Triste'),
    ]
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="reacciones")
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, related_name="reacciones")
    tipo = models.CharField(max_length=50, choices=TIPOS_REACCION)
    fecha = models.DateTimeField(default=now)

    def __str__(self):
        """
        Retorna una representación de la reacción, mostrando el tipo y el nombre completo del ciudadano.

        Returns:
            str: El tipo de reacción seguido del nombre del ciudadano.
        """
        return f"{self.tipo} - {self.ciudadano.nombre_completo}"
