from django.contrib import admin
from ciudadano_app.models import *

# Register your models here.
@admin.register(AreaComunal)
class AreaComunal(admin.ModelAdmin):
    list_display = ('nombre_area', 'hora_de_apertura', 'hora_de_cierre')

@admin.register(Reserva)
class Reserva(admin.ModelAdmin):
    list_display = ('area_comunal', 'fecha_reserva', 'hora_inicio', 'hora_fin', 'tipo_reserva', 'ciudadano')

@admin.register(Ciudadano)
class Ciudadano(admin.ModelAdmin):
    list_display = ('nombre_completo',)
