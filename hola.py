import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "servicios_ciudadanos.settings")
django.setup()

from entidad_municipal_app.models import EspacioPublico, EntidadMunicipal

def main():
    # Assuming you have already created or have an existing EntidadMunicipal
    entidad_email = "entidad@test.com"
    entidad = EntidadMunicipal.objects.get(correo_electronico=entidad_email)

    # Create a new EspacioPublico
    nuevo_espacio, creado = EspacioPublico.objects.get_or_create(
        nombre="Nuevo Espacio Cultural",
        defaults={
            "direccion": "Calle Nueva 789",
            "descripcion": "Espacio para eventos culturales y artísticos",
            "entidad_municipal": entidad,
            "estado_espacio_publico": "DISPONIBLE"
        }
    )

    if creado:
        print(f"Nuevo EspacioPublico creado: {nuevo_espacio.nombre}")
    else:
        print("El EspacioPublico ya existe.")

if __name__ == "__main__":
    main()