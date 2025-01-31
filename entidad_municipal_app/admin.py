from django.contrib import admin
from entidad_municipal_app.models import EntidadMunicipal

@admin.register(EntidadMunicipal)
class EntidadMunicipalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')  # Asegúrate de que todos los campos existan en el modelo
