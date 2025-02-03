"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views
from shared.views.logout import logout_usuario
from .views.eventos.evento import actualizar_asistencia, eliminar_inscripcion

urlpatterns = [
    path('', views.bienvenida_entidad, name='bienvenida_entidad'),
    path('login/', views.login_entidad, name='login_entidad'),
    path('logout/', logout_usuario, name='logout_entidad'),
    path('dashboard/', views.dashboard_entidad, name='dashboard_entidad'),
    path('eventos/', views.gestor_eventos, name='gestor_eventos'),
    path('eventos/<int:evento_id>/', views.evento, name='detalle_evento'),
    path('eventos/asistencia/<int:registro_id>/', actualizar_asistencia, name='actualizar_asistencia'),
    path('eventos/inscripcion/<int:registro_id>/', eliminar_inscripcion, name='eliminar_inscripcion'),
]
