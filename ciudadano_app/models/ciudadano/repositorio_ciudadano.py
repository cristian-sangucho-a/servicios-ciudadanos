from abc import ABC, abstractmethod
from typing import Optional
from .ciudadano import Ciudadano

class RepositorioCiudadano(ABC):
    """
    Clase abstracta que define la interfaz para el repositorio de ciudadanos.
    """
    
    @abstractmethod
    def crear_ciudadano(self, correo_electronico: str, nombre_completo: str, numero_identificacion: str) -> Ciudadano:
        """
        Método abstracto para crear y guardar un nuevo ciudadano.

        Args:
            correo_electronico (str): Correo electrónico del ciudadano
            nombre_completo (str): Nombre completo del ciudadano
            numero_identificacion (str): Número de identificación del ciudadano

        Returns:
            Ciudadano: La instancia del ciudadano creado
        """
        pass

    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Ciudadano]:
        """
        Método abstracto para obtener un ciudadano por su ID.

        Args:
            id (int): ID del ciudadano a buscar

        Returns:
            Optional[Ciudadano]: El ciudadano encontrado o None si no existe
        """
        pass

    @abstractmethod
    def obtener_por_correo(self, correo_electronico: str) -> Optional[Ciudadano]:
        """
        Método abstracto para obtener un ciudadano por su correo electrónico.

        Args:
            correo_electronico (str): Correo electrónico del ciudadano

        Returns:
            Optional[Ciudadano]: El ciudadano encontrado o None si no existe
        """
        pass

    @abstractmethod
    def obtener_por_identificacion(self, numero_identificacion: str) -> Optional[Ciudadano]:
        """
        Método abstracto para obtener un ciudadano por su número de identificación.

        Args:
            numero_identificacion (str): Número de identificación del ciudadano

        Returns:
            Optional[Ciudadano]: El ciudadano encontrado o None si no existe
        """
        pass
