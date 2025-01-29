from typing import Optional, Dict
from django.contrib.auth.models import User
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano
from ciudadano_app.models.ciudadano.repositorio_ciudadano import RepositorioCiudadano

class RepositorioCiudadanoEnMemoria(RepositorioCiudadano):
    """
    Una implementación de repositorio que almacena ciudadanos en memoria.
    También guarda en la base de datos para mantener las relaciones.
    """

    def __init__(self):
        self.ciudadanos: Dict[int, Ciudadano] = {}
        self.ciudadanos_por_correo: Dict[str, Ciudadano] = {}
        self.ciudadanos_por_identificacion: Dict[str, Ciudadano] = {}
        self.siguiente_id = 1

    def crear_ciudadano(self, correo_electronico: str, nombre_completo: str, numero_identificacion: str) -> Ciudadano:
        """
        Crea y guarda un nuevo ciudadano en memoria y en la base de datos.

        Args:
            correo_electronico (str): Correo electrónico del ciudadano
            nombre_completo (str): Nombre completo del ciudadano
            numero_identificacion (str): Número de identificación del ciudadano

        Returns:
            Ciudadano: La instancia del ciudadano creado
        """
        # Verificar si ya existe un ciudadano con el mismo correo o identificación
        if correo_electronico in self.ciudadanos_por_correo:
            raise ValueError("Ya existe un ciudadano con ese correo electrónico")
        if numero_identificacion in self.ciudadanos_por_identificacion:
            raise ValueError("Ya existe un ciudadano con ese número de identificación")

        # Crear el usuario de Django
        usuario = User.objects.create_user(
            username=correo_electronico,
            email=correo_electronico,
            password="sws@12345."  # En producción se generaría una contraseña aleatoria
        )

        # Crear el ciudadano y guardarlo en la base de datos
        ciudadano = Ciudadano(
            usuario=usuario,
            correo_electronico=correo_electronico,
            nombre_completo=nombre_completo,
            numero_identificacion=numero_identificacion
        )
        ciudadano.save()
        
        # Asignar ID y guardar en los diccionarios en memoria
        self.ciudadanos[ciudadano.id] = ciudadano
        self.ciudadanos_por_correo[correo_electronico] = ciudadano
        self.ciudadanos_por_identificacion[numero_identificacion] = ciudadano
        
        return ciudadano

    def obtener_por_id(self, id: int) -> Optional[Ciudadano]:
        """
        Obtiene un ciudadano por su ID.

        Args:
            id (int): ID del ciudadano a buscar

        Returns:
            Optional[Ciudadano]: El ciudadano encontrado o None si no existe
        """
        return self.ciudadanos.get(id)

    def obtener_por_correo(self, correo_electronico: str) -> Optional[Ciudadano]:
        """
        Obtiene un ciudadano por su correo electrónico.

        Args:
            correo_electronico (str): Correo electrónico del ciudadano

        Returns:
            Optional[Ciudadano]: El ciudadano encontrado o None si no existe
        """
        return self.ciudadanos_por_correo.get(correo_electronico)

    def obtener_por_identificacion(self, numero_identificacion: str) -> Optional[Ciudadano]:
        """
        Obtiene un ciudadano por su número de identificación.

        Args:
            numero_identificacion (str): Número de identificación del ciudadano

        Returns:
            Optional[Ciudadano]: El ciudadano encontrado o None si no existe
        """
        return self.ciudadanos_por_identificacion.get(numero_identificacion)
