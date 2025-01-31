#language: es

  Característica: Organizar eventos públicos masivos
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
  Y la fecha del evento es "06/02/2025"
  Cuando el espacio público "Plaza de la Cultura" no se encuentre disponible
  Entonces no se creara el evento
  Y se mostrarán los espacios públicos disponibles


Esquema del escenario: Cancelar evento debido a caso fortuito externo
   Dado que existe un evento llamado "<nombre_evento>" con el estado "<estado_evento>"
   Y el espacio público destinado al evento "<nombre_espacio>" está en una situación de "<estado_espacio>" debido a un "<motivoRiesgo>"
   Cuando la entidad municipal cambia el estado del evento a "<nuevo_estado_evento>"
   Entonces se registra el motivo de la cancelación "<resultado>"

   Ejemplos:
    | nombre_evento                   | estado_evento | nombre_espacio         | estado_espacio | motivoRiesgo       | nuevo_estado_evento | resultado                                                       |
    | Festival Cultural de Primavera  | PROGRAMADO    | Parque Bicentenario    | Afectado       | Incendio Forestal  | CANCELADO           | Se registra la cancelación con motivo "Incendio Forestal"       |
    | Festival Cultural de Primavera  | PROGRAMADO    | Parque Bicentenario    | No Afectado    | Incendio Forestal  | PROGRAMADO          | El espacio no está afectado, no aplica cancelación              |
    | Evento Inexistente              | NULL          | NULL                   | NULL           | NULL               | NULL                | No existe evento a cancelar                                     |
    | Festival Cultural de Primavera  | EN_CURSO      | Parque Bicentenario    | Afectado       | Incendio Forestal  | EN_CURSO            | No se puede cancelar, evento en curso                           |
    | Festival Cultural de Primavera  | FINALIZADO    | Parque Bicentenario    | Afectado       | Incendio Forestal  | FINALIZADO          | No se puede cancelar, evento finalizado                         |

