#Created by jona
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

    Escenario: Resolver un nuevo reporte
        Dado un reporte ciudadano "R001" del problema "Luminaria pública dañada" llega al "SIAC"
        Y el reporte ha sido asignado automaticamente al departamento "EPMMOP" por tener un nivel de confianza mayor que el 80%
        Y el reporte tiene el estado "asignado"
        Cuando el departamento asignado atienda el reporte con mayor prioridad
        Entonces el estado del reporte atendido cambia a "resuelto"
        Y el departamento debe registrar la evidencia "foco quemado ha sido cambiado" de la solucion del reporte.
        Y el estado del resto de reportes no atendidos cambia a "postergado"

#    Escenario: Postergar reporte
#        Dado un reporte ciudadano "id_reporte" del problema "descripcion_problema"
#        #Y su nivel de confianza de clasificacion es mayor que el 80% para cualquier departamento
#        Y el reporte es asignado al departamento "nombre_departamento" por tener un nivel de confianza mayor que el 80%
#        #Cuando los recursos del departamento asignado no sean suficientes para resolver el problema
#        Cuando la prioridad del reporte no sea la mas alta del conjunto de reportes no atendidos
#        Entonces el estado del reporte cambia a "postergado"

    Escenario: Resolver un reporte postergado
        Dado un reporte ciudadano "R002" del problema "Bache en la calle" asignado al departamento "EPMMOP"
        Y el reporte tiene el estado "postergado"
        Cuando el departamento asignado atienda el reporte con mayor prioridad
        Entonces el estado del reporte atendido cambia a "resuelto"
        Y el departamento debe registrar la evidencia "se ha rellenado el bache" de la solucion del reporte.
        Y el estado del resto de reportes no atendidos cambia a "postergado"


    Escenario: Asignacion manual
        Dado un reporte ciudadano "R003" del problema "consultar lugar de votacion" llega al "SIAC"
        Y no ha sido asignado a ningun departamento
        Cuando se realice una clasificacion manual al departamento "EPMMOP"
        Entonces el estado del reporte cambia a "asignado"
        Y se añaden los nuevos criterios de clasificación "criterio1, criterio2, criterio3"
