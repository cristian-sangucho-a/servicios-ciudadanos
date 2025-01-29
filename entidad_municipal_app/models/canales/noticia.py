from django.db import models
from django.utils.timezone import now
from .canal_informativo import CanalInformativo

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