from django.urls import path
from . import views
from shared.views.logout import logout_usuario

urlpatterns = [
    # URLs para autenticación de ciudadano
    path('', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('dashboard/', views.dashboard_ciudadano, name='dashboard_ciudadano'),
    path('bienvenida/', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('login/', views.login_ciudadano, name='login_ciudadano'),
    path('logout/', logout_usuario, name='logout_ciudadano'),
    path('reporte/', views.envio_reporte, name='envio_reporte'),
]
