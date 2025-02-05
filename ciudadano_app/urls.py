from django.urls import path
from . import views
from .views.canales.noticia import reaccionar, comentar, conteo_reacciones
from .views.canales.suscripcion import suscribirse_canal, desuscribirse_canal
from .views.canales.notificacion import listar_notificacion
from .views.canales.canales import lista_canales, detalle_canal, ver_noticias
from shared.views.logout import logout_usuario
from .views.eventos.lista_eventos import (
    lista_eventos,
    inscribirse_evento,
    cancelar_inscripcion,
    lista_espera_evento,
    confirmar_inscripcion_evento
)

urlpatterns = [
    path('canal/<int:canal_id>/suscribirse/', suscribirse_canal, name='suscribirse_canal'),
    path('canal/<int:canal_id>/desuscribirse/', desuscribirse_canal, name='desuscribirse_canal'),
    path('canal/<int:canal_id>/detalle/', detalle_canal, name='detalle_canal'),
    path('canal/lista_canales/', lista_canales, name='lista_canales'),
    path('muro/', ver_noticias, name='ver_noticias'),
    path('notificaciones/', listar_notificacion, name='ver_notificaciones'),
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
    path('agenda/', views.agenda, name='agenda'),
    path('reserva/', views.reservar, name='reservar_area_comunal'),
    path('areas_comunales/', views.cargar_areas, name='cargar_areas_comunales'),
    path('calendario/', views.cargar_calendario, name='cargar_calendario'),
    path('logout/', logout_usuario, name='logout_ciudadano'),
    path('obtener-reservas/', views.obtener_reservas_por_fecha, name='obtener_reservas_por_fecha'),
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar_reserva/', views.cancelar_reserva, name='cancelar_reserva'),

    # URLs para eventos
    path('eventos/', lista_eventos, name='lista_eventos'),
    path('eventos/<int:evento_id>/inscribirse/', inscribirse_evento, name='inscribirse_evento'),
    path('eventos/<int:evento_id>/confirmar/', confirmar_inscripcion_evento, name='confirmar_inscripcion_evento'),
    path('eventos/<int:evento_id>/cancelar/', cancelar_inscripcion, name='cancelar_inscripcion'),
    path('eventos/<int:evento_id>/lista-espera/', lista_espera_evento, name='lista_espera_evento'),

    # URLs para reportes
    path('reporte/', views.reportes_view, name='reportes'),
    path('reporte/enviar/', views.envio_reporte, name='envio_reporte'),

    # Nuevas URLs para sectores y notificaciones
    path('agregar-sectores/', views.agregar_sectores_ciudadano, name='agregar_sectores'),
    path('listar_sectores/', views.listar_sectores_ciudadano, name='listar_sectores'),
    path('eliminar-sector/<int:sector_id>/', views.eliminar_sector_ciudadano, name='eliminar_sector'),

    path('notificacion_de_estado/', views.listar_notificaciones_ciudadano, name='ver_estado_sector'),
    path('notificacion_de_estado/', views.notificar_reporte_alta_prioridad_ciudadano, name='ver_estado_sector'),
    path('notificacion_de_estado/', views.notificar_estado_riesgo_ciudadano, name='ver_estado_sector'),

]