# services/servicio_de_estado_sector.py
from datetime import timedelta

from django.utils.timezone import now

# Palabras clave asociadas a cada estado
PALABRAS_CLAVE_ESTADOS = {
    "RIESGO": ["peligro", "robo", "asalto", "violencia", "crimen"],
    "PRECAUCIÓN": ["cuidado", "precaución", "alerta", "riesgo moderado"],
    "SEGURO": ["seguro", "tranquilo", "sin incidentes"],
}

class ServicioDeEstadoSector:
    def __init__(self, sector):
        self.sector = sector

    def actualizar_estado(self):
        # Obtener reportes de los últimos 30 días
        reportes = self.sector.reporte_set.filter(fecha_reporte__gte=now() - timedelta(days=30))
        total_reportes = reportes.count()

        # Contadores de reportes según gravedad
        conteo = {"RIESGO": 0, "PRECAUCIÓN": 0, "SEGURO": 0}

        for reporte in reportes:
            asunto_lower = reporte.asunto.lower()
            for estado, palabras_clave in PALABRAS_CLAVE_ESTADOS.items():
                if any(palabra in asunto_lower for palabra in palabras_clave):
                    conteo[estado] += 1
                    break  # Solo contar en una categoría

        # Lógica para determinar el estado del sector
        if conteo["RIESGO"] >= 3 or total_reportes >= 20:
            self.sector.estado = "RIESGO"
        elif conteo["PRECAUCIÓN"] >= 3 or total_reportes >= 10:
            self.sector.estado = "PRECAUCIÓN"
        else:
            self.sector.estado = "SEGURO"

        self.sector.save()
