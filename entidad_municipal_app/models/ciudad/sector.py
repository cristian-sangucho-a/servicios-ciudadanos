class Sector:
    def __init__(self, nombre_sector):
        self.nombre_sector = nombre_sector
        self.estado = "Normal"
        self.ubicacion = None  # Puede ser una tupla (lat, lon)

    def set_estado(self, estado):
        self.estado = estado