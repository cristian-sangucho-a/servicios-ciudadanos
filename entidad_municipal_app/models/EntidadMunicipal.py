"""
Modelo para representar una entidad municipal.
"""
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class EntidadMunicipalManager(BaseUserManager):
    def create_user(self, correo_electronico, password=None, **extra_fields):
        if not password:
            raise ValueError('The password must be set')
        if not correo_electronico:
            raise ValueError('The Email field must be set')
        user = self.model(correo_electronico=self.normalize_email(correo_electronico), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, correo_electronico, password=None, **extra_fields):
        if not password:
            raise ValueError('The password must be set')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(correo_electronico, password, **extra_fields)

class EntidadMunicipal(AbstractBaseUser, PermissionsMixin):  # Add PermissionsMixin
    correo_electronico = models.EmailField(unique=True, help_text="Correo electrónico de la entidad")
    nombre = models.CharField(max_length=100, help_text="Nombre de la entidad municipal")
    direccion = models.CharField(max_length=200, help_text="Dirección física de la entidad")
    telefono = models.CharField(max_length=20, help_text="Número de teléfono de contacto")
    fecha_registro = models.DateTimeField(auto_now_add=True, help_text="Fecha de registro en el sistema")

    is_active = models.BooleanField(default=True, help_text="Indica si la entidad está activa")
    is_staff = models.BooleanField(default=False, help_text="Indica si la entidad tiene acceso al panel de administración")

    groups = models.ManyToManyField(
        'auth.Group',
        related_name="entidad_municipal_groups",  # Custom related name to avoid conflicts
        blank=True,
        help_text="The groups this user belongs to.",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="entidad_municipal_permissions",  # Custom related name to avoid conflicts
        blank=True,
        help_text="Specific permissions for this user.",
    )

    objects = EntidadMunicipalManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre', 'direccion', 'telefono']

    def __str__(self):
        return f"Entidad Municipal: {self.nombre}"
