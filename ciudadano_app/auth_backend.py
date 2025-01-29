"""
Backend de autenticación personalizado para el sistema de servicios municipales.
"""
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
import logging

# Configurar el logger
logger = logging.getLogger(__name__)

class EmailBackend(ModelBackend):
    """
    Backend de autenticación que permite a los usuarios iniciar sesión usando su correo electrónico.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autentica a un usuario usando su correo electrónico y contraseña.
        
        Args:
            request: Objeto request de Django
            username: En este caso, será el correo electrónico del usuario
            password: Contraseña del usuario
            **kwargs: Argumentos adicionales
            
        Returns:
            Usuario autenticado o None si la autenticación falla
        """
        UserModel = get_user_model()
        email = kwargs.get('email') or username
        
        # Log de los datos recibidos
        logger.debug(f"Intento de autenticación - Email recibido: {email}")
        logger.debug(f"Datos adicionales (kwargs): {kwargs}")
        logger.debug(f"Username recibido: {username}")
        
        if email is None:
            logger.warning("No se proporcionó email")
            return None
            
        try:
            # Intentamos obtener el usuario por su correo electrónico
            logger.debug(f"Buscando usuario con email: {email}")
            user = UserModel.objects.get(email=email)
            
            # Log del resultado de la autenticación
            if user.check_password(password):
                logger.debug("Contraseña correcta")
                if self.user_can_authenticate(user):
                    logger.info(f"Usuario autenticado exitosamente: {email}")
                    return user
                else:
                    logger.warning(f"Usuario no está activo: {email}")
            else:
                logger.warning(f"Contraseña incorrecta para: {email}")
                
        except UserModel.DoesNotExist:
            logger.warning(f"No se encontró usuario con email: {email}")
            return None
            
        return None

    def get_user(self, user_id):
        """
        Obtiene un usuario por su ID.
        
        Args:
            user_id: ID del usuario a obtener
            
        Returns:
            Usuario si existe y está activo, None en caso contrario
        """
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(pk=user_id)
            return user if self.user_can_authenticate(user) else None
        except UserModel.DoesNotExist:
            return None
