from entidad_municipal_app.models.departamento.departamento import Departamento
from entidad_municipal_app.models.departamento.repositorio_departamento import RepositorioDepartamento

class ServicioDepartamento:
    """
    Servicio que gestiona la lógica de negocio de los departamentos.
    """

    def __init__(self, repositorio_departamento: RepositorioDepartamento):
        """
        Inicializa el servicio con un repositorio de departamentos.

        Args:
            repositorio_departamento (RepositorioDepartamento): Instancia del repositorio de departamentos.
        """
        self.repositorio_departamento = repositorio_departamento

    def registrar_departamento(self, nombre: str, descripcion: str = "") -> Departamento:
        """
        Registra un nuevo departamento en el sistema.

        Args:
            nombre (str): Nombre del departamento.
            descripcion (str, optional): Descripción del departamento. Por defecto, una cadena vacía.

        Returns:
            Departamento: La instancia del departamento registrado.

        Raises:
            ValueError: Si ya existe un departamento con el mismo nombre.
        """
        if self.repositorio_departamento.obtener_departamento_por_nombre(nombre):
            raise ValueError("Ya existe un departamento con este nombre.")
        nuevo_departamento = Departamento(nombre=nombre, descripcion=descripcion)
        self.repositorio_departamento.agregar_departamento(nuevo_departamento)
        return nuevo_departamento

    def obtener_departamentos(self) -> list[Departamento]:
        """
        Obtiene todos los departamentos registrados.

        Returns:
            list[Departamento]: Lista de todos los departamentos registrados.
        """
        return self.repositorio_departamento.listar_departamentos()

    def obtener_departamento_por_nombre(self, nombre: str) -> Departamento | None:
        """
        Obtiene un departamento por su nombre.

        Args:
            nombre (str): Nombre del departamento a buscar.

        Returns:
            Departamento | None: Instancia del departamento si existe, de lo contrario, None.
        """
        return self.repositorio_departamento.obtener_departamento_por_nombre(nombre)
