# Created by intel at 24/01/2025
# language: es

Característica: Realización de actividades por ciudadanos
  Como entidad publica
  Quiero que los ciudadanos realicen actividades en mis espacios publicos
  Para mejorar la convivencia entre los ciudadanos

  Escenario: Reserva de un area comunal para actividad pública
    Dado que existen areas comunales disponibles en el espacio publico "Parque la Alameda" en la ciudad y son
      | Nombre            |
      | Cancha #1         |
      | Cancha #2         |
      | Cancha #3         |
    Y el ciudadano no supera las "3" reservas activas
    Cuando el ciudadano realice una reserva "publica" en el area comunal "Cancha #1" el "15/01/2024" de "16:00" a "17:00"
    Entonces se guarda la reserva en la Agenda Pública
    #TODO: Cooordinar con Marco la publicacion o suscripcion para notificar esta reserva

  Escenario: Reserva de un area comunal para una actividad privada
    Dado que existen areas comunales disponibles en el espacio publico "Parque la Alameda" en la ciudad y son
      | Nombre    |
      | Cancha #1 |
      | Cancha #2 |
      | Cancha #3 |
    Cuando el ciudadano realice una reserva "privada" en el area comunal "Cancha #2" el "15/01/2024" de "10:00" a "12:00"
    Y agregue los correos de los invitados "jean.cotera@epn.edu, cristian.sangucho@epn.edu.ec" a la reserva
    Entonces se guarda la reserva en la Agenda Pública
    Y se enviará una invitación por correo con los detalles de la reserva.

    #TODO: las vistas se deben narrar en los test para representar un cambio de estado de mi sistema??????????????????????????????? TIPO DE RESERVA

  Escenario: Cancelar reserva de actividad publica en area comunal
    Dado que el ciudadano tiene una reserva "publica" en el espacio publico "Parque la Alameda" en el area comunal "Cancha #3" el "15/01/2024" de "16:00" a "17:00"
    Cuando cancele la reserva
    Entonces la reserva será eliminada de la agenda pública.

  Escenario: Cancelar reserva de actividad privada en area comunal
    Dado que el ciudadano tiene una reserva "privada" en el espacio publico "Parque la Alameda" en el area comunal "Cancha #3" el "15/01/2024" de "7:00" a "8:00"
    Cuando cancele la reserva
    Entonces se enviará una correo de cancelacion a los invitados
    Y la reserva será eliminada de la agenda pública.
    #TODO: un metodo que elimine y notifique a los invitados para mantener la consistencia de la informacion
