from entidad_municipal_app.models.departamento.departamento import Departamento
from entidad_municipal_app.models.departamento.repositorio_departamento import RepositorioDepartamento

class ServicioDepartamento():
    """
    Servicio que gestiona la lógica de negocio de los departamentos.
    """

    def __init__(self, repositorio_departamento: RepositorioDepartamento):
        self.repositorio_departamento = repositorio_departamento

    def registrar_departamento(self, nombre: str, descripcion: str = ""):
        if self.repositorio_departamento.obtener_departamento_por_nombre(nombre):
            raise ValueError("Ya existe un departamento con este nombre.")
        nuevo_departamento = Departamento(nombre=nombre, descripcion=descripcion)
        self.repositorio_departamento.agregar_departamento(nuevo_departamento)
        return nuevo_departamento

    def obtener_departamentos(self):
        """
        Obtiene todos los departamentos registrados.

        :return: Lista de todos los departamentos.
        """
        return self.repositorio_departamento.listar_departamentos()

    def obtener_departamento_por_nombre(self, nombre: str):
        """
        Obtiene un departamento por su nombre.

        :param nombre: Nombre del departamento a buscar.
        :type nombre: str
        :return: Instancia de Departamento o None si no existe.
        """
        return self.repositorio_departamento.obtener_departamento_por_nombre(nombre)
