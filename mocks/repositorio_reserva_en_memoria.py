from ciudadano_app.admin import Ciudadano
from ciudadano_app.models import Reserva
from ciudadano_app.models.repositorio_reserva import RespositorioReserva
from entidad_municipal_app.models import EspacioPublico, espacio_publico


class RepositorioReservaMemoria(RespositorioReserva):
    def __init__(self):
        self.base_datos = {}
        self.contador_reservas = 0
        self.areas_por_espacio = {}  # {EspacioPublico: [AreaComunal]}
        self.reservas_ciudadano_list = []
        self.contador_ids = 0  # Simular autoincremento de IDs


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

        self.reservas_ciudadano_list.append(nueva_reserva)
        return self.contador_reservas, True

    def ciudadano_supera_maximo_reservas(self, ciudadano):
        reservas_ciudadano = [1,2]
        return len(reservas_ciudadano) >= 3

    def hay_areas_comunales_disponibles(self, espacio_publico):
        return len(self.areas_por_espacio.get(espacio_publico, [])) > 0

    def agregar_area_comunal(self, area_comunal, espacio_publico):
        # Asignar un ID simulado
        self.contador_ids += 1
        area_comunal.id = self.contador_ids

        # Simular la relación
        if espacio_publico not in self.areas_por_espacio:
            self.areas_por_espacio[espacio_publico] = []
        self.areas_por_espacio[espacio_publico].append(area_comunal)

    def obtener_area_comunal(self, id_area_comunal):
        for espacio in self.areas_por_espacio.items():
            for area in espacio:
                if area.id == id_area_comunal:
                    return area  # Devuelve la primera área comunal encontrada
        return None  # Si no hay áreas disponibles, devuelve None

    def obtener_reserva_por_id(self, id_reserva):
        for reserva in self.reservas_ciudadano_list:
            if reserva.id == id_reserva:
                return reserva


    def cancelar_reserva(self, id_reserva, ciudadano):
        reserva = self.obtener_reserva_por_id(id_reserva)
        if reserva and reserva['ciudadano'] == ciudadano:
            self.reservas_ciudadano_list.remove(reserva)
            return True
        return False

    def enviar_invitacion(self, reserva):

        print(f'''
        From: Servicios
        To: ${reserva.correos_invitados}

        Estan cordialmente invitados a ${reserva}
        ''')