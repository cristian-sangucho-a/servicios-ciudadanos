"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('eventos/<int:evento_id>/', views.detalle_evento, name='detalle_evento'),
    path('eventos/<int:evento_id>/inscribir/', views.inscribir_evento, name='inscribir_evento'),
    path('eventos/registro/<int:registro_id>/cancelar/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    path('eventos/<int:evento_id>/lista-espera/', views.lista_espera, name='lista_espera'),
]
