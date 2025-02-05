# language: es
# encoding: utf-8

Característica: Organizar eventos públicos masivos
  Como Entidad Municipal
  Quiero organizar eventos públicos masivos en los espacios públicos
  para promover la participación ciudadana y el uso eficiente de los recursos públicos.


Escenario: Organizar un evento en un espacio público disponible
  Dado que una entidad municipal desea organizar un evento
  Y la fecha del evento es "2024-02-15 10:00:00"
  Cuando el espacio público "Parque Central" se encuentre en estado DISPONIBLE
  Entonces se creara el evento
  Y cambiara el estado del espacio público


Escenario: Organizar un evento en un espacio público no disponible
  Dado que una entidad municipal desea organizar un evento
  Y la fecha del evento es "2024-02-15 10:00:00"
  Cuando el espacio público "Plaza de la Cultura" se encuentra en estado NO_DISPONIBLE
  Entonces no se creara el evento
  Y se mostrarán los espacios públicos disponibles

Escenario: Programar un evento cuando un cantidad minima de participantes confirmen su asistencia
  Dado que una entidad municipal desea organizar un evento
  Y la fecha del evento es "2024-02-15 10:00:00"
  Cuando se cumple el minimo de "1" cuidadanos para crear el evento
  Entonces se actualizara el estado del evento


Esquema del escenario: Cancelar evento debido a caso fortuito externo
   Dado que existe un evento llamado "<nombre_evento>" con el estado "<estado_evento>"
   Y el espacio público destinado al evento es "<espacio_publico>"
   Cuando el espacio publico esta en situación de "<estado_espacio>" debido a un "<motivo_riesgo>"
   Entonces se registra el motivo de la cancelación
   Y la entidad municipal cambia el estado del evento a "<estado_evento_final>"


   Ejemplos:
    | nombre_evento                | estado_evento | espacio_publico      | estado_espacio | motivo_riesgo      | estado_evento_final |
    | Festival Cultural            | PROGRAMADO    | Parque Bicentenario  | AFECTADO      | Incendio Forestal  | CANCELADO          |
    | Concierto de Rock           | PROGRAMADO    | Parque Bicentenario  | AFECTADO      | Incendio Forestal  | CANCELADO          |
    | Feria de Emprendimiento     | PROGRAMADO    | Parque Bicentenario  | AFECTADO      | Incendio Forestal  | CANCELADO          |
    | Evento de Caridad           | PROGRAMADO    | Parque Bicentenario  | AFECTADO      | Incendio Forestal  | CANCELADO          |
    | Evento Inexistente          | NULL          | NULL                 | NULL          | NULL               | NULL               |
