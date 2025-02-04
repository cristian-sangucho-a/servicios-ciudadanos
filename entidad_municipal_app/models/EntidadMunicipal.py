from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class EntidadMunicipalManager(BaseUserManager):
    """Manager personalizado para el modelo EntidadMunicipal."""

    def create_user(self, correo_electronico, password=None, **extra_fields):
        """Crea y devuelve un usuario con el correo electrónico y contraseña proporcionados.

        Args:
            correo_electronico (str): Dirección de correo electrónico del usuario.
            password (str, optional): Contraseña del usuario. Defaults to None.
            **extra_fields: Campos adicionales para el usuario.

        Raises:
            ValueError: Si no se proporciona una contraseña o un correo electrónico.

        Returns:
            EntidadMunicipal: Instancia del usuario creado.
        """
        if not password:
            raise ValueError('The password must be set')
        if not correo_electronico:
            raise ValueError('The Email field must be set')

        user = self.model(correo_electronico=self.normalize_email(correo_electronico), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, password=None, **extra_fields):
        """Crea y devuelve un superusuario con los permisos correspondientes.

        Args:
            correo_electronico (str): Dirección de correo electrónico del superusuario.
            password (str, optional): Contraseña del superusuario. Defaults to None.
            **extra_fields: Campos adicionales para el superusuario.

        Raises:
            ValueError: Si los atributos is_staff o is_superuser no son True.

        Returns:
            EntidadMunicipal: Instancia del superusuario creado.
        """
        if not password:
            raise ValueError('The password must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(correo_electronico, password, **extra_fields)

class EntidadMunicipal(AbstractBaseUser, PermissionsMixin):
    """Modelo que representa una entidad municipal en el sistema."""

    correo_electronico = models.EmailField(unique=True, help_text="Correo electrónico de la entidad")
    nombre = models.CharField(max_length=100, help_text="Nombre de la entidad municipal")
    direccion = models.CharField(max_length=200, help_text="Dirección física de la entidad")
    telefono = models.CharField(max_length=20, help_text="Número de teléfono de contacto")
    fecha_registro = models.DateTimeField(auto_now_add=True, help_text="Fecha de registro en el sistema")

    is_active = models.BooleanField(default=True, help_text="Indica si la entidad está activa")
    is_staff = models.BooleanField(default=False, help_text="Indica si la entidad tiene acceso al panel de administración")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="entidad_municipal_groups",  # Nombre de relación personalizado para evitar conflictos
        blank=True,
        help_text="Grupos a los que pertenece este usuario.",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="entidad_municipal_permissions",  # Nombre de relación personalizado para evitar conflictos
        blank=True,
        help_text="Permisos específicos para este usuario.",
    )

    objects = EntidadMunicipalManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre', 'direccion', 'telefono']

    def __str__(self):
        """Representación en cadena del modelo.

        Returns:
            str: Nombre de la entidad municipal.
        """
        return f"Entidad Municipal: {self.nombre}"
