"""
Gestor personalizado para el modelo Ciudadano.
"""
from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

class GestorCiudadano(BaseUserManager):
    """Gestor para la creación y administración de ciudadanos en el sistema"""
    
    def create_user(self, correo_electronico, password, **campos_adicionales):
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
            raise ValidationError('El correo electrónico es obligatorio para crear un ciudadano')
        if not password:
            raise ValidationError('La contraseña es obligatoria para crear un ciudadano')

        correo_normalizado = self.normalize_email(correo_electronico)

        ciudadano = self.model(correo_electronico=correo_normalizado, **campos_adicionales)

        ciudadano.set_password(password)

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
