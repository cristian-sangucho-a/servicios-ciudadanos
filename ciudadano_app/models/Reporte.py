# from typing import Any

# from django.db import models

from ciudadano_app.models import Ciudadano
from ciudadano_app.models.TipoReporte import TipoReporte


class Reporte():

    def __init__(self, ciudadano: Ciudadano, tipo_reporte: TipoReporte, **kwargs):
        # super().__init__(*args, **kwargs)
        self.__ciudadano = ciudadano
        self.__tipo_reporte = tipo_reporte
        self.__prioridad = None
        if kwargs.get("ubicacion"):
            self.__ubicacion = kwargs.get("ubicacion")

    def validar_reporte(self) -> bool:
        es_valido = bool(self.__ciudadano and self.__tipo_reporte and self.__ubicacion)
        return es_valido

    @property
    def ciudadano(self):
        return self.__ciudadano

    @property
    def tipo_reporte(self):
        return self.__tipo_reporte

    @property
    def ubicacion(self):
        return self.__ubicacion

    @property
    def prioridad(self):
        return self.__prioridad

    @prioridad.setter
    def prioridad(self, prioridad: int):
        if prioridad < 1 or prioridad > 5:
            raise ValueError("La prioridad debe estar entre 1 y 5.")
        self.__prioridad = prioridad
