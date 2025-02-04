# models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from shared.models import ServicioDeNotificacion
from shared.models.notificacion.servicio_de_estado_sector import ServicioDeEstadoSector

# Lista de sectores disponibles
SECTORES = [
    ('BELISARIO QUEVEDO', 'Belisario Quevedo'),
    ('EL INCA', 'El Inca'),
    ('CARCELÉN', 'Carcelén'),
    ('CENTRO HISTÓRICO', 'Centro Histórico'),
    ('CHILIBULO', 'Chilibulo'),
    ('CHILLOGALLO', 'Chillogallo'),
    ('CHIMBACALLE', 'Chimbacalle'),
    ('COCHAPAMBA', 'Cochapamba'),
    ('COMITÉ DEL PUEBLO', 'Comité del Pueblo'),
    ('CONCEPCIÓN', 'Concepción'),
    ('COTOCOLLAO', 'Cotocollao'),
    ('EL CONDADO', 'El Condado'),
    ('MAGDALENA', 'Magdalena'),
    ('GUAMANÍ', 'Guamaní'),
    ('IÑAQUITO', 'Iñaquito'),
    ('ITCHIMBÍA', 'Itchimbía'),
    ('JIPIJAPA', 'Jipijapa'),
    ('KENNEDY', 'Kennedy'),
    ('LA ARGELIA', 'La Argelia'),
    ('LA ECUATORIANA', 'La Ecuatoriana'),
    ('LA FERROVIARIA', 'La Ferroviaria'),
    ('LA LIBERTAD', 'La Libertad'),
    ('LA MENA', 'La Mena'),
    ('MARISCAL SUCRE', 'Mariscal Sucre'),
    ('PONCEANO', 'Ponceano'),
    ('PUENGASÍ', 'Puengasí'),
    ('QUITUMBE', 'Quitumbe'),
    ('RUMIPAMBA', 'Rumipamba'),
    ('SAN BARTOLO', 'San Bartolo'),
    ('SAN JUAN', 'San Juan'),
    ('SOLANDA', 'Solanda'),
    ('TURUBAMBA', 'Turubamba'),
]

# Definición de los estados posibles del sector
ESTADOS_SECTOR = [
    ('SEGURO', 'Seguro'),
    ('PRECAUCIÓN', 'Precaución'),
    ('RIESGO', 'Riesgo'),
]

class Sector(models.Model):
    nombre = models.CharField(
        max_length=100,
        choices=SECTORES,
        unique=True,
        verbose_name=_("Nombre del Sector"),  # Nombres más descriptivos
        help_text=_("Nombre único del sector")  # Ayuda en el formulario
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_SECTOR,
        default='SEGURO',
        verbose_name=_("Estado del Sector"),
        help_text=_("Estado actual del sector (Seguro, Precaución, Riesgo)")
    )

    def __str__(self):
        return self.nombre

    def actualizar_estado_y_notificar(self):
        servicio_estado = ServicioDeEstadoSector(self)
        estado_anterior = self.estado
        servicio_estado.actualizar_estado()  # Calcula el nuevo estado

        if self.estado != estado_anterior:  # Si hubo un cambio de estado
            servicio_notificacion = ServicioDeNotificacion()
            for ciudadano in self.ciudadanos_interesados.all():  # Notifica a interesados
                servicio_notificacion.notificar_estado_riesgo(ciudadano, self)
