from django.db import models
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from .noticia import Noticia
from django.utils.timezone import now

class Comentario(models.Model):
    """
    Comentarios de ciudadanos en publicaciones.

    Este modelo permite a los ciudadanos dejar comentarios en las noticias publicadas.
    Cada comentario está vinculado a una noticia y un ciudadano específico.

    Attributes:
        noticia (ForeignKey): La noticia a la que se le ha agregado el comentario.
        ciudadano (ForeignKey): El ciudadano que ha dejado el comentario.
        contenido (str): El contenido del comentario.
        fecha (datetime): La fecha y hora en que se registró el comentario. Se establece automáticamente a la fecha actual.
    """
    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="comentarios")
    ciudadano = models.ForeignKey(Ciudadano, on_delete=models.CASCADE, related_name="comentarios")
    contenido = models.TextField()
    fecha = models.DateTimeField(default=now)

    def __str__(self):
        """
        Retorna una representación del comentario, mostrando el nombre del ciudadano y el inicio del contenido del comentario.

        Returns:
            str: Un comentario con el nombre del ciudadano y los primeros 30 caracteres del contenido.
        """
        return f"Comentario de {self.ciudadano.nombre_completo}: {self.contenido[:30]}"
