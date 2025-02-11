# language: es

Característica: Enviar y gestionar reporte por parte de un ciudadano
  Como ciudadano
  Quiero enviar un reporte de un problema en mi comunidad
  Para que el sistema determine la frecuencia del problema y asigne una prioridad automáticamente en una escala del 1 al 5.

  Esquema del escenario: Enviar un reporte
    Dado que un ciudadano llamado "<nombre>" con correo "<correo>" e identificación "<identificacion>" ha identificado un problema
    Y proporciona sus detalles en un reporte con asunto "<asunto>", descripción "<descripcion>" y ubicación "<ubicacion>"
    Cuando se envía el reporte descrito
    Y se asigna una prioridad de acuerdo a "<cantidad_registro>" registros previos del problema con asunto "<asunto>"
    Entonces el reporte es asignado con prioridad "<prioridad>"

    Ejemplos:
      | nombre     | correo              | identificacion | asunto       | descripcion | ubicacion | cantidad_registro | prioridad |
      | Juan Perez | juan.perez@test.com | 1727263717     | inundacion   | Se inundo   | Av. 123   | 13                | 1         |
      | Juan Perez | juan.perez@test.com | 1727263717     | incendio     | Se inundo   | Av. 123   | 8                 | 2         |
      | Juan Perez | juan.perez@test.com | 1727263717     | electricidad | Se inundo   | Av. 123   | 5                 | 3         |
      | Juan Perez | juan.perez@test.com | 1727263717     | bache        | Se inundo   | Av. 123   | 3                 | 4         |
      | Juan Perez | juan.perez@test.com | 1727263717     | robo         | Se inundo   | Av. 123   | 1                 | 5         |
      | Juan Perez | juan.perez@test.com | 1727263717     | choque       | Se inundo   | Av. 123   | 0                 | 5         |

  Escenario: Confirmar reporte existente
    Dado que un ciudadano llamado "Juan Perez" con correo "juan.perez@test.com" e identificación "1727263717" visualice el reporte con asunto "explosion" y ubicación "Av. 123"
    Y el reporte cuente con "12" de registros previos de dicho reporte y prioridad "2"
    Cuando se confirma el reporte
    Y se crea un nuevo reporte con el mismo "explosion", "Av. 123" y "Se quemo"
    Y se asigna una prioridad de acuerdo a "13" registros previos del problema con asunto "explosion"
    Entonces el reporte es asignado con prioridad "1"