# Created by intel at 24/01/2025
# language: es

Característica: Realización de actividades por ciudadanos
  Como entidad publica
  Quiero que los ciudadanos realicen actividades en mis espacios publicos
  Para mejorar la convivencia entre los ciudadanos

  Escenario: Reserva de espacio disponible para actividad pública
    Dado que existen espacios públicos disponibles en la ciudad y son
      | Nombre            |
      | Parque la Alameda |
      | La Carolina       |
      | Bicentenario      |
    Cuando el ciudadano reserve el espacio publico "Parque la Alameda" el "15/01/2024" de "16:00" a "15:00"
    Entonces se publicará la reserva en la Agenda Pública.

  Escenario: Reserva de un espacio público para una actividad privada
    Dado que existen espacios públicos disponibles en la ciudad y son
      | Nombre            |
      | Parque la Alameda |
      | La Carolina       |
      | Bicentenario      |
    Cuando el ciudadano reserve el espacio publico "Parque la Alameda" el "15/01/2024" de "16:00" a "15:00"
    Y agregue los correos de los invitados "jean.cotera@epn.edu, cristian.sangucho@epn.edu.ec" a la reserva
    Entonces se enviará una invitación por correo con los detalles de la reserva.

  Escenario: Cancelar reserva de actividad pública
    Dado que el ciudadano tiene una reserva en el "Parque la Alameda"
    Cuando cancele la reserva
    Entonces la reserva será eliminada de la agenda pública.

