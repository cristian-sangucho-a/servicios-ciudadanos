#language: es

Característica: Manejar los reportes ciudadanos
    Como entidad publica,
    quiero clasificar, atender y posponer los reportes enviados por los ciudadanos,
    para asignar recursos de manera eficiente y solucionar los problemas en el menor tiempo posible.

    #Estados de los reportes
        # no_asignado
        # asignado
        # postergado
        # resuelto


    Escenario: Resolver reportes asignados a un departamento
        Dado nuevos reportes que llegan al gestor de departamentos
        | nombre     | correo              | identificacion | asunto       | descripcion | ubicacion | cantidad_registro | prioridad |
        | Juan Perez | juan.perez@test.com | 1727263717     | inundacion   | Se inundo   | Av. 123   | 13                | 1         |
        | Juan Perez | juan.perez@test.com | 1727263717     | incendio     | Se inundo   | Av. 123   | 8                 | 2         |
        Y los reportes han sido asignados automáticamente a un departamento
        Y los reportes son priorizados por su asunto
        Cuando el departamento "EPMMOP" atienda el reporte "1"
        Entonces el departamento registra la evidencia "Basura recogida" de la solución del reporte atendido
        Y el estado del reporte atendido cambia a "resuelto"


    Escenario: Resolver reportes postergados de un departamento
        Dado nuevos reportes que llegan al gestor de departamentos
        Y el departamento "EPMMOP" posterga el reporte "2"
        Cuando el departamento "EPMMOP" atienda el reporte "2"
        Entonces el departamento registra la evidencia "Se ha rellenado el bache" de la solución del reporte atendido
        Y el estado del reporte atendido cambia a "resuelto"
