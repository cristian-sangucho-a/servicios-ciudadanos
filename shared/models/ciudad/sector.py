from django.db import models

# Definición de los estados posibles del sector
ESTADOS_SECTOR = {
    "Seguro": [
        "grafiti", "ruido excesivo", "basura acumulada", "luminaria dañada"
    ],
    "Precaución": [
        "robo", "asalto", "pelea callejera", "vandalismo",
        "bache", "poste caído", "semáforo dañado",
        "choque leve", "inundación", "deslizamiento leve"
    ],
    "Riesgo": [
        "homicidio", "secuestro", "violación", "ataque armado",
        "colapso de vía", "hundimiento", "incendio estructural",
        "choque múltiple", "deslizamiento severo", "inundación de calle",
        "corte total de carretera", "derrumbes"
    ]
}

class Sector(models.Model):
    # Atributos
    nombre = models.CharField(max_length=100, unique=True)
    latitud = models.FloatField()
    longitud = models.FloatField()
    estado = models.CharField(max_length=50, choices=ESTADOS_SECTOR, default="Seguro")
    ciudad = models.ForeignKey('Ciudad', related_name='sectores', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

    # Métodos
    def actualizar_estado(self, servicio_de_estado_sector):
        """
        Método para actualizar el estado del sector.
        """
        servicio_de_estado_sector.actualizar_estado()
