"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views
from shared.views.logout import logout_usuario

urlpatterns = [
    path('', views.bienvenida_entidad, name='bienvenida_entidad'),
    path('login/', views.login_entidad, name='login_entidad'),
    path('logout/', logout_usuario, name='logout_entidad'),
    path('dashboard/', views.dashboard_entidad, name='dashboard_entidad'),
    path('eventos/', views.gestor_eventos, name='gestor_eventos'),
    path('eventos/<int:evento_id>/', views.evento, name='evento'),
    path('eventos/<int:evento_id>/editar_evento/', views.editar_evento, name='editar_evento'),
    path('eventos/crear_evento/', views.crear_evento, name='crear_evento'),

]
