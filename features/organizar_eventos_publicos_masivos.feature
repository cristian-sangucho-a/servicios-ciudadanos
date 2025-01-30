#language: es

  Característica: Organizar eventos publicos masivos
    Como Entidad Municipal
    Quiero organizar eventos públicos masivos en los espacios públicos
    para promover la participación ciudadana y el uso eficiente de los recursos públicos.


Escenario: Organizar un evento en un espacio público disponible
  Dado que la entidad municipal "Municipio de Quito" desea organizar el evento "Quito Fest"
  Y la fecha del evento es "2023-12-06" con hora de inicio a las "14:00"
  Cuando el espacio público "Parque Central" se encuentre disponible
  Entonces se publicará el evento en la Agenda Pública


Escenario: Organizar un evento en un espacio público no disponible
  Dado que la entidad municipal "Municipio de Quito" desea organizar el evento "Quito Fest"
  Y la fecha del evento es "2023-12-06" con hora de inicio a las "14:00"
  Cuando el espacio público "Parque Central" no se encuentre disponible
  Entonces no se incluirá el evento en la Agenda Pública
  Y se mostrarán los espacios públicos disponibles


Escenario: Organizar un evento en múltiples espacios públicos simultáneamente
  Dado que la entidad municipal "Municipio de Quito" desea organizar el evento "Quito Fest"
  Y la fecha del evento es "2023-12-06" con hora de inicio a las "14:00"
  Cuando se registran mas de un espacio público para el evento
  Y todos los espacios públicos son distintos entre sí
  Entonces se incluirá el evento en la Agenda Pública


Escenario: Cancelar evento debido a caso fortuito externo
  Dado que existe un evento llamado "Festival Cultural de Primavera" con el estado "Confirmado"
  Y el espacio público destinado al evento está en una situación de "Riesgo" debido a un "Incendio forestal"
  Cuando la entidad municipal cambia el estado del evento a "Cancelado"
  Entonces se registra el motivo de la cancelación


Escenario: Organizar un evento en un espacio público disponible nuevo
  Dado que una entidad municipal desea organizar un evento
  Y la fecha deseada del evento es 06/02/2025 14:00
  Cuando se añada el espacio público "Parque Central" que se encuentra disponible
  Entonces se agregara el evento en la Agenda Pública
