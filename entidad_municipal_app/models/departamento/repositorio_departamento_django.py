from entidad_municipal_app.models.departamento.departamento import Departamento
from entidad_municipal_app.models.departamento.repositorio_departamento import RepositorioDepartamento

class RepositorioDepartamentoDjango(RepositorioDepartamento):
    """Implementación de la interfaz RepositorioDepartamento usando Django ORM."""

    def obtener_departamento_por_nombre(self, nombre: str) -> Departamento | None:
        """Obtiene un departamento por su nombre utilizando Django ORM.

        Args:
            nombre (str): Nombre del departamento a buscar.

        Returns:
            Departamento | None: Instancia del departamento si existe, None si no se encuentra.
        """
        return Departamento.objects.filter(nombre=nombre).first()

    def listar_departamentos(self) -> list[Departamento]:
        """Lista todos los departamentos en la base de datos.

        Returns:
            list[Departamento]: Lista de todos los departamentos.
        """
        return list(Departamento.objects.all())

    def agregar_departamento(self, departamento: Departamento) -> None:
        """Agrega un nuevo departamento a la base de datos.

        Args:
            departamento (Departamento): Instancia del departamento a agregar.
        """
        departamento.save()

    def actualizar_descripcion_departamento(self, nombre: str, nueva_descripcion: str) -> None:
        """Actualiza la descripción de un departamento en la base de datos.

        Args:
            nombre (str): Nombre del departamento a actualizar.
            nueva_descripcion (str): Nueva descripción del departamento.
        """
        Departamento.objects.filter(nombre=nombre).update(descripcion=nueva_descripcion)
