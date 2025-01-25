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