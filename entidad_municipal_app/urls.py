"""
URLs para la aplicación de entidad municipal.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.bienvenida_entidad, name='bienvenida_entidad'),
    path('login/', views.login_entidad, name='login_entidad'),
    path('dashboard/', views.dashboard_entidad, name='dashboard_entidad'),
    path('eventos/', views.lista_eventos, name='lista_eventos'),
    path('reportes/', views.lista_todos_reportes, name='lista_todos_reportes'),
    path('reportes/<str:departamento>/', views.lista_reportes_por_departamento, name='lista_reportes_por_departamento'),
    path('reportes/<int:reporte_id>/postergar/', views.postergar_reporte, name='postergar_reporte'),
    # path('reportes/<str:departamento>/', views.reportes_por_departamento, name='reportes_por_departamento'),
    path('reportes/<int:reporte_id>/resolver/', views.resolver_reporte, name='resolver_reporte'),
]
