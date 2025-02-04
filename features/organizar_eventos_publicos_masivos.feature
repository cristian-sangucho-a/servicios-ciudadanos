#language: es

  Característica: Organizar eventos públicos masivos
    Como Entidad Municipal
    Quiero organizar eventos públicos masivos en los espacios públicos
    para promover la participación ciudadana y el uso eficiente de los recursos públicos.


Escenario: Organizar un evento en un espacio público disponible
  Dado que una entidad municipal desea organizar un evento
  Y la fecha del evento es "06/02/2025"
  Cuando el espacio público "Parque Central" se encuentre en estado "DISPONIBLE"
  Entonces se creara el evento
  Y cambiara el estado del espacio público


Escenario: Organizar un evento en un espacio público no disponible
  Dado que una entidad municipal desea organizar un evento
  Y la fecha del evento es "06/02/2025"
  Cuando el espacio público "Plaza de la Cultura" se encuentra en estado "NO_DISPONIBLE"
  Entonces no se creara el evento
  Y se mostrarán los espacios públicos disponibles


Esquema del escenario: Cancelar evento debido a caso fortuito externo
   Dado que existe un evento llamado "<nombre_evento>" con el estado "<estado_evento>"
   Y el espacio público destinado al evento es "<nombre_espacio>"
   Cuando el espacio publico esta en situación de "<estado_espacio>" debido a un "<motivoRiesgo>"
   Entonces se registra el motivo de la cancelación
   Y la entidad municipal cambia el estado del evento a "<nuevo_estado_evento>"


   Ejemplos:
    | nombre_evento                   | estado_evento | nombre_espacio         | estado_espacio | motivoRiesgo       | nuevo_estado_evento |
    | Festival Cultural de Primavera  | PROGRAMADO    | Parque Bicentenario    | Afectado       | Incendio Forestal  | CANCELADO           |
    | Festival Cultural de Primavera  | PROGRAMADO    | Parque Bicentenario    | Afectado       | Incendio Forestal  | CANCELADO           |
    | Evento Inexistente              | NULL          | NULL                   | NULL           | NULL               | NULL                |
    | Festival Cultural de Primavera  | EN_CURSO      | Parque Bicentenario    | Afectado       | Incendio Forestal  | CANCELADO           |
    | Festival Cultural de Primavera  | FINALIZADO    | Parque Bicentenario    | Afectado       | Incendio Forestal  | CANCELADO           |

