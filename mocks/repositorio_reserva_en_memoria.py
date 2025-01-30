from ciudadano_app.admin import Ciudadano
from ciudadano_app.models.repositorio_reserva import RespositorioReserva
from entidad_municipal_app.models import EspacioPublico


class RepositorioReservaMemoria(RespositorioReserva):
    def __init__(self):
        self.base_datos = {}
        self.reservas = []
        self.contador_reservas = 0
        self.espacios_publicos = {}


    def reservar_area_comunal(self, area_comunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva, ciudadano):
        self.contador_reservas += 1
        nueva_reserva = {
            'id': self.contador_reservas,
            'area_comunal': area_comunal,
            'fecha_reserva': fecha_reserva,
            'hora_inicio': hora_inicio,
            'hora_fin': hora_fin,
            'tipo_reserva': tipo_reserva,
            'ciudadano': ciudadano
        }
        self.reservas.append(nueva_reserva)
        return self.contador_reservas, True

    def ciudadano_supera_maximo_reservas(self, ciudadano):
        reservas_ciudadano = [1,2]
        return len(reservas_ciudadano) >= 3

    def hay_areas_comunales_disponibles(self, espacio_publico):
        return len(self.espacios_publicos.get(espacio_publico, [])) > 0

    def agregar_area_comunal(self, area_comunal, espacio_publico):
        if espacio_publico not in self.espacios_publicos:
            self.espacios_publicos[espacio_publico] = []
        self.espacios_publicos[espacio_publico].append(area_comunal)