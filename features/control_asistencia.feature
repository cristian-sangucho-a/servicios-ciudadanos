# language: es

Característica: Controlar la asistencia a eventos masivos
  Como entidad municipal
  Quiero habilitar un sistema de registro previo a eventos masivos
  Para controlar el aforo y garantizar la seguridad de los asistentes

  Escenario: Registro exitoso dentro del límite de aforo
    Dado que existe un evento con aforo disponible
    Y el ciudadano cumple con los requisitos de inscripción
    Cuando el ciudadano intenta registrarse en el evento
    Entonces el sistema debe permitir el registro
    Y enviar una confirmación de inscripción por correo electrónico
    Y reducir un cupo disponible del evento

  Escenario: Intento de registro cuando el evento está lleno
    Dado que existe un evento con aforo lleno
    Cuando un ciudadano intenta registrarse en el evento
    Entonces el sistema debe rechazar el registro directo
    Y agregar al ciudadano a una lista de espera
    Y notificar al ciudadano de su estado en la lista de espera

  Escenario: Cancelación de inscripción por parte del ciudadano
    Dado que un ciudadano está inscrito en un evento
    Y hay otro ciudadano en lista de espera
    Cuando el ciudadano decide cancelar su inscripción
    Entonces el sistema debe liberar el cupo correspondiente
    Y el primer ciudadano en lista de espera debe ser registrado automáticamente
    Y notificar al ciudadano promovido de la lista de espera
