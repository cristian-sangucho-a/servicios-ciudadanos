from django.urls import path
from .views import landing_page, logout_usuario, error_session

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('logout/', logout_usuario, name='logout_usuario'),
    path('error_session/', error_session, name='error_session'),
]