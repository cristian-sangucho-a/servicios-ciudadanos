from ciudadano_app.admin import Ciudadano
from ciudadano_app.models.repositorio_reserva import RespositorioReserva
from entidad_municipal_app.models import EspacioPublico


class RepositorioReservaMemoria(RespositorioReserva):

    def __init__(self):
        self.base_datos = []

    # AQUI, EN ESTA CLASE, PROBAMOS EL CONCEPTO QUE DEBE SER TESTEADO
    def reservar_area_comunal(self, area_comunal, fecha_reserva, hora_inicio, hora_fin, tipo_reserva, ciudadano):
        return 1, True

    def ciudadano_supera_maximo_reservas(self, ciudadano):
        return False

    def crear_ciudadano(self, nombre, correo):
        pass

    def hay_areas_comunales_disponibles(self, espacio_publico: EspacioPublico):
        self.base_datos[espacio_publico] = [espacio_publico.areas_comunales]
        return len(self.base_datos[espacio_publico]) > 0
