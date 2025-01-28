from django.db import models
from django.utils.timezone import now
from ciudadano_app.models import Ciudadano
from entidad_municipal_app.models.canales.canal_informativo import CanalInformativo


class Noticia(models.Model):
    """
    Publicaciones generales asociadas a canales informativos.

    Este modelo representa una noticia que es publicada en un canal informativo.
    Las noticias contienen un título, contenido, fecha de publicación y, opcionalmente, una imagen asociada.

    Attributes:
        canal (ForeignKey): El canal informativo al cual pertenece la noticia.
        titulo (str): El título de la noticia.
        contenido (str): El contenido completo de la noticia.
        fecha_publicacion (datetime): La fecha y hora en que se publicó la noticia. Se establece automáticamente a la fecha actual.
        imagen (ImageField, optional): Una imagen opcional asociada a la noticia.

    Meta:
        verbose_name: "Noticia"
        verbose_name_plural: "Noticias"
        ordering: ["-fecha_publicacion"]
    """
    canal = models.ForeignKey(CanalInformativo, on_delete=models.CASCADE, related_name="noticias")
    titulo = models.CharField(max_length=255)
    contenido = models.TextField()
    fecha_publicacion = models.DateTimeField(default=now)
    imagen = models.ImageField(upload_to="noticias/", null=True, blank=True)

    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ["-fecha_publicacion"]

    def __str__(self):
        """
        Retorna el título de la noticia junto con el nombre del canal al que pertenece.

        Returns:
            str: El título de la noticia seguido del nombre del canal.
        """
        return f"{self.titulo} - {self.canal.nombre}"


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
