"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views
from.views.canales import gestion_canal

urlpatterns = [
    path('', views.bienvenida_entidad, name='bienvenida_entidad'),
    path('lista_canales', gestion_canal.listar_canales_administrados, name='listar_canales_administrados'),
    path('login/', views.login_entidad, name='login_entidad'),
    path('dashboard/', views.dashboard_entidad, name='dashboard_entidad'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
]
