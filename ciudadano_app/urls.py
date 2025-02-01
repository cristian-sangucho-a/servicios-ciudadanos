from django.urls import path
from . import views

urlpatterns = [
    # URLs para autenticación de ciudadano
    path('', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('dashboard/', views.dashboard_ciudadano, name='dashboard_ciudadano'),
    path('bienvenida/', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('login/', views.login_ciudadano, name='login_ciudadano'),
    path('logout/', views.logout_ciudadano, name='logout_ciudadano'),
    path('agenda/', views.agenda, name='agenda'),
    path('reserva/', views.reserva, name='reservar_area_comunal'),
    path('areas_comunales/', views.cargar_areas, name='cargar_areas_comunales'),
    path('calendario/', views.cargar_calendario, name='cargar_calendario'),
]
