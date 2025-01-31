"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_entidad, name='login_entidad'),
    path('bienvenida/', views.bienvenida_entidad, name='bienvenida_entidad'),
]
