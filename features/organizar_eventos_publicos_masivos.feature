#language: es

  Característica: Organizar eventos publicos masivos
    Como Entidad Municipal
    Quiero organizar eventos públicos masivos en los espacios públicos
    para promover la participación ciudadana y el uso eficiente de los recursos públicos.


Escenario: Organizar un evento en un espacio público disponible nuevo
  Dado que una entidad municipal desea organizar un evento
  Y la fecha deseada del evento es 06/02/2025 14:00
  Cuando se añada el espacio público "Parque Central" que se encuentra disponible
  Entonces se agregara el evento en la Agenda Pública
