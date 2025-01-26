"""
Modelo de Ciudadano para el sistema municipal.
"""
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class GestorCiudadano(BaseUserManager):
    """Gestor para la creación y administración de ciudadanos en el sistema"""
    
    def create_user(self, correo_electronico, contrasena=None, **campos_adicionales):
        """
        Crea un nuevo ciudadano regular en el sistema.
        
        Args:
            correo_electronico: Correo electrónico del ciudadano
            contrasena: Contraseña del ciudadano
            campos_adicionales: Campos adicionales como nombre, identificación, etc.
        
        Returns:
            Ciudadano: Nueva instancia de Ciudadano
            
        Raises:
            ValueError: Si no se proporciona un correo electrónico
        """
        if not correo_electronico:
            raise ValueError('El correo electrónico es obligatorio para crear un ciudadano')
            
        correo_normalizado = self.normalize_email(correo_electronico)
        ciudadano = self.model(correo_electronico=correo_normalizado, **campos_adicionales)
        ciudadano.set_password(contrasena)
        ciudadano.save(using=self._db)
        return ciudadano

    def create_superuser(self, correo_electronico, contrasena=None, **campos_adicionales):
        """
        Crea un nuevo ciudadano con privilegios de administrador.
        
        Args:
            correo_electronico: Correo electrónico del administrador
            contrasena: Contraseña del administrador
            campos_adicionales: Campos adicionales como nombre, identificación, etc.
            
        Returns:
            Ciudadano: Nueva instancia de Ciudadano con privilegios de administrador
        """
        campos_adicionales.setdefault('es_staff', True)
        campos_adicionales.setdefault('is_superuser', True)
        return self.create_user(correo_electronico, contrasena, **campos_adicionales)

class Ciudadano(AbstractBaseUser, PermissionsMixin):
    """
    Modelo que representa a un ciudadano en el sistema municipal.
    Extiende el modelo base de usuario de Django para incluir campos específicos.
    """
    
    correo_electronico = models.EmailField(
        unique=True,
        verbose_name='Correo Electrónico',
        help_text='Dirección de correo electrónico del ciudadano'
    )
    
    nombre_completo = models.CharField(
        max_length=120,
        verbose_name='Nombre Completo',
        help_text='Nombre completo del ciudadano'
    )
    
    numero_identificacion = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Número de Identificación',
        help_text='Número de documento de identidad del ciudadano'
    )
    
    esta_activo = models.BooleanField(
        default=True,
        verbose_name='¿Está Activo?',
        help_text='Indica si el ciudadano puede acceder al sistema'
    )
    
    es_staff = models.BooleanField(
        default=False,
        verbose_name='¿Es Personal Administrativo?',
        help_text='Indica si el ciudadano puede acceder al panel de administración'
    )
    
    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de Registro',
        help_text='Fecha y hora en que el ciudadano se registró en el sistema'
    )

    objects = GestorCiudadano()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre_completo', 'numero_identificacion']

    class Meta:
        verbose_name = 'Ciudadano'
        verbose_name_plural = 'Ciudadanos'
        ordering = ['-fecha_registro']

    def obtener_nombre_completo(self):
        """Retorna el nombre completo del ciudadano"""
        return self.nombre_completo

    def obtener_correo_electronico(self):
        """Retorna el correo electrónico del ciudadano"""
        return self.correo_electronico

    def obtener_identificacion(self):
        """Retorna el número de identificación del ciudadano"""
        return self.numero_identificacion

    def __str__(self):
        return f"Ciudadano: {self.nombre_completo} ({self.correo_electronico})"
