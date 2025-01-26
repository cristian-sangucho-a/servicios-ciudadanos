# Created by ASUS at 24/1/2025
# language: es
Característica: Notificar incidentes relevantes o el estado de un sector de mi interés
  Como ciudadano,
  Quiero recibir notificaciones de incidentes relevantes o el estado de sectores de interés
  Para poder tomar decisiones informadas y evitar situaciones de riesgo

  Escenario: Registrar sector de interés
    Dado que existen sectores en la ciudad y son
      | nombre_sector |
      | La Floresta   |
      | Chillogallo   |
      | La Magdalena  |
      | Solanda       |
      | La Mariscal   |
    Cuando el ciudadano "Andrés Cantuña" seleccione el sector "Solanda" como de interés
    Entonces se agregará a la lista de sectores de interés

  Escenario: Notificar sobre un incidente relevante en un sector de interés
    Dado que el ciudadano "Andrés Cantuña" tiene registrado el sector "Solanda" como de interés
    Cuando se reporta un incidente del tipo "Accidente"
    Entonces se enviará una notificación por correo con los detalles del incidente

  Escenario: Notificar sobre un incidente reportado en un sector cercano a mi ubicación actual
    Cuando se reporta un incidente en un sector a menos de 2 kilómetros de mi ubicación actual
    Y el incidente sea del tipo "Accidente"
    Entonces se enviará una notificación por correo con los detalles del incidente
    Y la notificación debe incluir la distancia aproximada al incidente

  Escenario: Notificar cuando el estado de un sector de interés sea de riesgo
    Dado que el ciudadano "Andrés Cantuña" tiene registrado el sector "Solanda" como de interés
    Cuando se reportan al menos "5" incidentes del tipo "Inseguridad"
    Entonces el sector cambiará a estado "Riesgo"
    Y se enviará una notificación por correo con el mensaje "Precaución: el sector Solanda ha sido catalogado como de riesgo."