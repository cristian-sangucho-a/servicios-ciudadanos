from django.urls import path
from . import views
from shared.views.logout import logout_usuario
from .views.eventos.lista_eventos import (
    lista_eventos, 
    inscribirse_evento, 
    cancelar_inscripcion, 
    lista_espera_evento
)

urlpatterns = [
    # URLs para autenticación de ciudadano
    path('', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('dashboard/', views.dashboard_ciudadano, name='dashboard_ciudadano'),
    path('bienvenida/', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('login/', views.login_ciudadano, name='login_ciudadano'),
    path('logout/', logout_usuario, name='logout_ciudadano'),
    path('eventos/', lista_eventos, name='lista_eventos'),
    path('eventos/<int:evento_id>/inscribirse/', inscribirse_evento, name='inscribirse_evento'),
    path('eventos/<int:evento_id>/cancelar/', cancelar_inscripcion, name='cancelar_inscripcion'),
    path('eventos/<int:evento_id>/lista-espera/', lista_espera_evento, name='lista_espera_evento'),
]
