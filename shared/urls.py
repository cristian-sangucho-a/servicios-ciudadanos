from django.urls import path
from .views import landing_page, logout_usuario

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('logout/', logout_usuario, name='logout_usuario'),
]