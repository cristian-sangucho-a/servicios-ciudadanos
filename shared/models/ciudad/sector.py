# models.py
from django.db import models

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
        unique=True
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS_SECTOR,
        default='SEGURO'
    )

    def __str__(self):
        return self.nombre
