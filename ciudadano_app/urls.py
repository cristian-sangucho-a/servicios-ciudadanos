from django.urls import path
from . import views
from .views.canales.noticia import reaccionar, comentar, conteo_reacciones
from .views.canales.suscripcion import suscribirse_canal
from .views.canales.suscripcion import desuscribirse_canal
from .views.canales.canales import lista_canales, detalle_canal, ver_noticias

urlpatterns = [
    path('canal/<int:canal_id>/suscribirse/', suscribirse_canal, name='suscribirse_canal'),
    path('canal/<int:canal_id>/desuscribirse/', desuscribirse_canal, name='desuscribirse_canal'),
    path('canal/<int:canal_id>/detalle/', detalle_canal, name='detalle_canal'),
    path('canal/lista_canales/', lista_canales, name='lista_canales'),
    path('muro/', ver_noticias, name='ver_noticias'),
    path('muro/reaccion/<int:noticia_id>', reaccionar, name='reaccionar'),
    path('muro/conteo/<int:noticia_id>/', conteo_reacciones, name='conteo_reacciones'),
    path('muro/comentario/<int:noticia_id>/', comentar, name='comentar'),
    # URLs para autenticación de ciudadano
    path('', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('dashboard/', views.dashboard_ciudadano, name='dashboard_ciudadano'),
    path('bienvenida/', views.bienvenida_ciudadano, name='bienvenida_ciudadano'),
    path('registro/', views.registro_ciudadano, name='registro_ciudadano'),
    path('login/', views.login_ciudadano, name='login_ciudadano'),
    path('logout/', views.logout_ciudadano, name='logout_ciudadano'),
]
