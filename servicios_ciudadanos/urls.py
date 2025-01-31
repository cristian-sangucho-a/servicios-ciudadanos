"""
URL configuration for servicios_ciudadanos project.
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

def redirect_to_login(request):
    return redirect('login_ciudadano')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_login, name='landing_page'),
    path('ciudadano/', include('ciudadano_app.urls')),
    path('entidad/', include('entidad_municipal_app.urls')),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing_page'), name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
