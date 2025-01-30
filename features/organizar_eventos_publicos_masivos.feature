#language: es

  Característica: Organizar eventos publicos masivos
    Como Entidad Municipal
    Quiero organizar eventos públicos masivos en los espacios públicos
    para promover la participación ciudadana y el uso eficiente de los recursos públicos.


Escenario: Organizar un evento en un espacio público disponible
  Dado que una entidad municipal desea organizar un evento
  Y la fecha del evento es "06/02/2025"
  Cuando el espacio público "Parque Central" que se encuentra disponible
  Entonces se creara el evento


Escenario: Organizar un evento en un espacio público no disponible
  Dado que una entidad municipal desea organizar un evento
  Y la fecha deseada del evento es 06/02/2025 14:00
  Cuando el espacio público "Parque Central" no se encuentre disponible
  Entonces no se incluirá el evento en la Agenda Pública
  Y se mostrarán los espacios públicos disponibles


 Escenario: Cancelar evento debido a caso fortuito externo
  Dado que existe un evento llamado "Festival Cultural de Primavera" con el estado "Confirmado"
  Y el espacio público destinado al evento está en una situación de "Riesgo" debido a un "Incendio forestal"
  Cuando la entidad municipal cambia el estado del evento a "Cancelado"
  Entonces se registra el motivo de la cancelación

