# from typing import Any

# from django.db import models

class TipoReporte():
    def __init__(self, asunto: str, descripcion: str):
        # super().__init__(*args, **kwargs)
        self.__asunto = asunto
        self.__descripcion = descripcion

    @property
    def asunto(self):
        return self.__asunto

    @property
    def descripcion(self):
        return self.__descripcion
