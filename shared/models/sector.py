from django.db import models

class Sector(models.Model):
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
        ('MAGDALENA', 'La Magdalena'),
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

    nombre = models.CharField(max_length=50, choices=SECTORES, unique=True)
    estado = models.CharField(max_length=20, default='NORMAL')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'Sector'
        verbose_name_plural = 'Sectores' 