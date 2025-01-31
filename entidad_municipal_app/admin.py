from django.contrib import admin
from entidad_municipal_app.models import EntidadMunicipal, EspacioPublico, EventoMunicipal, RegistroAsistencia

@admin.register(EspacioPublico)
class EspacioPublicoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'entidad_municipal')  # entidad_municipal debe ser una relación válida

@admin.register(EventoMunicipal)
class EventoMunicipalAdmin(admin.ModelAdmin):
    list_display = ('nombre_evento',)  # Coma al final para definirlo como tupla

@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ('estado_registro',)
    # Coma al final para definirlo como tupla
@admin.register(EntidadMunicipal)
class EntidadMunicipalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion', 'telefono')  # Asegúrate de que todos los campos existan en el modelo
