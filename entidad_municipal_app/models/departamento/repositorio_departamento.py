from abc import ABC, abstractmethod
from entidad_municipal_app.models.departamento.departamento import Departamento

class RepositorioDepartamento(ABC):
    """
    Clase abstracta que define la interfaz para la gestión de departamentos.
    """

    @abstractmethod
    def obtener_departamento_por_nombre(self, nombre: str):
        """
        Obtiene un departamento por su nombre.

        Args:
            nombre (str): Nombre del departamento a buscar.

        Returns:
            Departamento: Instancia del departamento si existe, None si no se encuentra.
        """
        pass

    @abstractmethod
    def listar_departamentos(self):
        """
        Lista todos los departamentos en la base de datos.

        Returns:
            list[Departamento]: Lista de todos los departamentos.
        """
        pass

    @abstractmethod
    def agregar_departamento(self, departamento: Departamento):
        """
        Agrega un nuevo departamento al sistema.

        Args:
            departamento (Departamento): Instancia del departamento a agregar.
        """
        pass

    @abstractmethod
    def actualizar_descripcion_departamento(self, nombre: str, nueva_descripcion: str):
        """
        Actualiza la descripción de un departamento.

        Args:
            nombre (str): Nombre del departamento a actualizar.
            nueva_descripcion (str): Nueva descripción del departamento.
        """
        pass
