from django.urls import path
from . import views

urlpatterns = [
    # URLs para autenticación de ciudadano
    path('login/', views.login_ciudadano, name='login_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('logout/', views.logout_ciudadano, name='logout_ciudadano'),
    path('bienvenida/', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
]
