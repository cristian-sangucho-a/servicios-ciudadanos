from django.contrib.auth.backends import BaseBackend
from ciudadano_app.models.ciudadano.ciudadano import Ciudadano

class CiudadanoBackend(BaseBackend):
    """
    Backend de autenticación para Ciudadano.
    Se basa en el campo 'correo_electronico' y la contraseña.
    """
    def authenticate(self, request, correo_electronico=None, password=None, **kwargs):
        print("\nDEBUG BACKEND DE AUTENTICACIÓN:")
        print(f"Intentando autenticar correo: {correo_electronico}")
        print(f"Contraseña recibida: {password}")

        try:
            user = Ciudadano.objects.get(correo_electronico=correo_electronico)
            print(f"Usuario encontrado: {user.nombre_completo}")
            print(f"Hash de contraseña almacenado: {user.password}")
            print(f"Verificando contraseña...")
            
            # Intentar verificar la contraseña
            is_valid = user.check_password(password)
            print(f"Resultado de check_password: {is_valid}")
            
            if is_valid:
                print("Contraseña correcta!")
                return user
            else:
                print("Contraseña incorrecta!")
                return None
                
        except Ciudadano.DoesNotExist:
            print("Usuario no encontrado en la base de datos")
            return None

    def get_user(self, user_id):
        try:
            return Ciudadano.objects.get(pk=user_id)
        except Ciudadano.DoesNotExist:
            return None
