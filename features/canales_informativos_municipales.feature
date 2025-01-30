# Created by LabP3E003 at 18/12/2024

# language: es

Característica: Canales informativos municipales
  Como entidad municipal,
  Quiero mantener informado sobre eventos y noticias locales mediante canales de interés,
  Para presentar las noticias más relevantes a los ciudadanos.

  Escenario: Canales de Noticias Locales Personalizados
    Dado que soy una entidad municipal que gestiona el canal "Cultura y arte",
    Cuando el ciudadano activa su suscripción al canal "Cultura y arte",
    Entonces el ciudadano recibe noticias relacionadas al canal.

  Escenario: Ciudadano reacciona y comenta en una noticia
    Dado existe un ciudadano registrado
    Y existe una noticia publicada en un canal informativo
    Cuando el ciudadano reacciona a la noticia con "Me gusta"
    Y el ciudadano comenta en la noticia con "Excelente noticia"
    Entonces la reacción y comentario del ciudadano quedan registrados en la noticia.

  Escenario: Canales de Emergencia
    Dado que soy una entidad municipal que gestiona el canal de "emergencia",
    Cuando ocurre un incidente "terremoto" en "Quito",
    Entonces el sistema envía alertas rápidas a los ciudadanos de "Quito".