"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views
from .views.canales import gestion_canal
from .views.canales import gestion_noticias

urlpatterns = [
    path('', views.bienvenida_entidad, name='bienvenida_entidad'),
    path('login/', views.login_entidad, name='login_entidad'),
    path('dashboard/', views.dashboard_entidad, name='dashboard_entidad'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('lista_canales/', gestion_canal.listar_canales_administrados, name='listar_canales_administrados'),
    path('crear_canal/', gestion_canal.crear_canal, name='crear_canal'),
    path('crear_canal_form/', gestion_canal.crear_canal_form, name='crear_canal_form'),
    path('eliminar_canal/<int:canal_id>', gestion_canal.eliminar_canal, name='eliminar_canal'),
    path('lista_canales/noticias_canal/<int:canal_id>', gestion_noticias.noticias_canal, name='noticias_canal'),
    path('lista_canales/noticias_canal/crear_noticia/<int:canal_id>', gestion_noticias.crear_noticia, name='crear_noticia'),
    path('lista_canales/noticias_canal/detalle_noticia/<int:noticia_id>', gestion_noticias.detalle_noticia, name='detalle_noticia'),
    path('lista_canales/noticias_canal/detalle_noticia/eliminar_noticia/<int:noticia_id>', gestion_noticias.eliminar_noticia, name='eliminar_noticia'),
]
