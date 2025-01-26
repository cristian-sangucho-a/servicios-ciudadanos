#language: es

  Característica: Organizar eventos publicos masivos

    Como entidad publica
    quiero organizar eventos públicos masivos en los espacios comunitarios
    para promover la participación ciudadana y el uso eficiente de los recursos públicos

Escenario: Organizar un evento en un lugar disponible
    Dado que la entidad municipal "Municipal Central" quiere organizar un evento "Quito Fest"
    Y el dia del evento "2023-07-15" y la hora inicio es "18:00"
    Cuando el lugar escogido es "Parque Central" Y esta disponible
    Entonces se publicara el evento en la Agenda Pública


Escenario: Organizar un evento en un lugar no disponible
    Dado que la entidad municipal "Municipal Central" quiere organizar un evento "Quito Fest"
    Y el dia del evento "2023-07-15" y la hora inicio es "18:00"
    Cuando el lugar escogido es "Parque Central"
    Y no esta disponible
    Entonces no se publicara el evento en la Agenda Pública
    Y se mostrara los lugares disponibles


Escenario: Organizar un evento en múltiples lugares simultáneamente
  Dado que la entidad municipal "<nombre de la entidad>" quiere organizar un evento "<nombre del evento>"
  Y el dia del evento "2023-07-15" y la hora inicio es "18:00"
  Cuando se registran varias ubicaciones para el evento:
    | Lugar          | Dirección                | Capacidad |
    | Parque Central | Av. Principal 123        | 500       |
    | Centro Cultural| Calle Secundaria 456     | 300       |
    | Estadio Municipal| Av. Deportes 789       | 1000     |
  Y estos son diferentes
  Entonces se publicara el evento en la Agenda Pública



Escenario: Cancelar evento debido a casos fortiutos/incidentes externos
  Dado el evento "Festival Cultural de Primavera" está en estado "Programado"
  Y la  del lugar esta "Peligro" debido a un incendio forestal
  Cuando la entidad municipal cambia el estado del evento a "Cancelado"
  Entonces la entidad municipal añade el motivo de cancelacion del evento

